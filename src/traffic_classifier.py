import influxdb, datetime, time
# Install me with: pip3 install sklearn
# We also need numpy: pip3 install numpy
# It should have been installed as a dependency nonetheless! 
from sklearn import svm

class gar_py:
	def __init__(self, host = 'localhost', port = 8086, kern_type = 'linear'):
		# Constructor n.n
		self.n_samples, self.traffic_mean = 0, 0
		self.host = host
		self.port = port
		self.dbname = 'telegraf'
		self.client = influxdb.InfluxDBClient(host, port, 'root', 'root', self.dbname)
		self.svm_inst = svm.SVC(kernel = kern_type)
		
		# We need to use these triple quotes so that we can use a tag within the query! 
		self.query = """select bytes_sent from net where interface = 's1-eth1' order by time desc limit 1;"""
		
		# Ejemplos de querys:
		# select icmp_inmsgs, icmp_outmsgs from net
		# select * from net where time >= '2019-12-31T00:00:00Z' and time < '2019-12-30T16:00:00Z'

		self.train_svm()

	def train_svm(self):
		# Dump data from a file and feed the SVM
		features, labels = [], []
		# Files are opened for reading and in text mode by default
		# Secifying it doesn't hurt though!
		# Our file format is: ^Sample_value, Current_mean, Class$
		# Where Class is either 0 (Not an attack) or 1 (Houston, we've got a situation!)
		# The ^ and $ characters symbolize the beginning and end of a line like in RegExps
		meal = open("SVM_training.txt", "rt")
		for line in meal:
			data_list = line.rsplit(", ")
			# We need to work with numbers. Casting time!
			for i in range(len(data_list)):
				data_list[i] = int(data_list[i])
			features.append(data_list[:2])
			labels.append(data_list[2])
		meal.close()
		self.svm_inst.fit(features, labels)
		
	def work_time(self):
		while True:
			# Note that the get_points() method returns a generator, we need to invoke
			# next() on it ourselves to work like this
			new_entry = next(self.get_data(self.query).get_points(measurement = 'net'))
			# Strings have been overloaded to allow
			# this type comparison!
			if new_entry['time'] > self.get_datetime():
				n_samples += 1
				# Take a look at the documentation for this quantity!
				delta_mean = (new_entry['icmp_inechos'] - mean) / (n_samples)
				mean += delta_mean
				if self.under_attack(new_entry['icmp_inechos'], mean):
					self.ring_the_alarm(True)
			time.sleep(2)
	
	def under_attack(self, ping_sample, current_mean):
		if self.svm_inst.predict([[ping_sample, current_mean]])[0] == 1:
			return True
		else:
			return False

	def get_data(self, petition):
		# Get data from InfluxDB
		return self.client.query(petition)

	def ring_the_alarm(self, should_i_ring):
		# Ring the alarm by writing to InfluxDB
		data_json = self.get_ddos_json_body(should_i_ring)
		if self.client.write_points(data_json):
			print('[OK] Data was correctly sent to InfluxDB :)')

	# --- Aux Methods --- #	
	def get_ddos_json_body(self, boolean):
		return [{'measurement': 'ddos', 'fields': {'value': boolean}, 'tags': {'host': 'Ryu_Controller'}, 'time': self.get_datetime()}]
	
	def get_datetime(self):
		return (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ')
 
if __name__ == "__main__":
	ai_bot = gar_py()
	
	# Unit test (DDoS alarm intf)
	print(ai_bot.get_datetime())
	print(ai_bot.get_ddos_json_body(True))
	ai_bot.ring_the_alarm(True)

	# Unit test (Query intf)
	print('Enviando esta query: ' + ai_bot.query)
	print('Resultado: \n' + str( ai_bot.get_data(ai_bot.query) ))	
	
	# Muchos datos, como los podemos procesar?
	data = ai_bot.get_data(ai_bot.query)
	for measurement in data.get_points(measurement = 'net'):
	
		bytes_sent = measurement['bytes_sent']
		print(str(bytes_sent))
	
	# tambien podemos filtrar por tag, en este caso solo estamos pidiendo de s1-eth1, pero podriamos hacer esto:
	#
	# get_points(tags={ 'interface': 's1-eth2'})
	#
	# O podemos hacer una mezcla:
	#
	# get_points(measurement='net',tags={ 'interface':'s2-eth1'})
	#
	#
	
	# Init
	ai_bot.work_time()
