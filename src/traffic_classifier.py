import influxdb, datetime, time, os, signal
# Install me with: pip3 install sklearn
# We also need numpy: pip3 install numpy
# It should have been installed as a dependency nonetheless! 
from sklearn import svm

class gar_py:
	def __init__(self, db_host = 'localhost', port = 8086, db = 'h4_net_stats', kern_type = 'linear', dbg = False):
		# Constructor n.n
		self.debug = dbg
		self.n_samples, self.mean = 0, 0
		self.host = db_host
		self.port = port
		self.dbname = db
		self.client = influxdb.InfluxDBClient(self.host, self.port, 'root', 'root', self.dbname)
		self.svm_inst = svm.SVC(kernel = kern_type)
		if os.uname()[1] == "pop-os":
			self.training_files = ["training_datasets/ICMP_data_class_0.csv", "training_datasets/ICMP_data_class_1.csv"]
		else:
			self.training_files = ["/home/vagrant/training_datasets/ICMP_data_class_0.csv", "/home/vagrant/training_datasets/ICMP_data_class_1.csv"]
		
		# We need to use these triple quotes so that we can use a tag within the query! 
		# self.query = """select bytes_sent from net where interface = 's1-eth1' order by time desc limit 1;"""
		self.query = """SELECT DERIVATIVE(icmp_inechos) AS d_ping FROM net ORDER BY time DESC LIMIT 3"""
		self.train_svm()

	def train_svm(self):
		# Dump data from a file and feed the SVM
		features, labels = [], []
		# Files are opened for reading and in text mode by default. Specifying it doesn't hurt though
		# Our file format is: ^Sample_value, Current_mean, Class$
		# Where Class is either 0 (Not an attack) or 1 (Houston, we've got a situation!)
		# The ^ and $ characters symbolize the beginning and end of a line like in RegExps
		for fname in self.training_files:
			meal = open(fname, "rt")
			for line in meal:
				data_list = line.rsplit(", ")
				# We need to work with numbers. Casting time!
				for i in range(len(data_list)):
					if i < 2:
						data_list[i] = float(data_list[i])
					else:
						data_list[i] = int(data_list[i])
				features.append(data_list[:2])
				labels.append(data_list[2])
			meal.close()
		if self.debug:
			print("Features first and last entries:\n\t", end = "")
			print(features[:1] + features[199:])
			print("Labels first and last entries:\n\t", end = "")
			print(labels[:1] + labels[199:])
		self.svm_inst.fit(features, labels)
		
	def work_time(self):
		last_entry_time = "0"
		while True:
			# We have to reverse the elements due to how the query returns the result. We need to
			# reverse() a list so that's why we need to cast the generator returned by get_points()
			for new_entry in reversed(list(self.get_data(self.query).get_points(measurement = 'net'))):
				# Strings have been overloaded to allow this type comparison!
				if new_entry['time'] > last_entry_time:
					last_entry_time = new_entry['time']
					self.n_samples += 1
					# Take a look at the documentation for this quantity!
					delta_mean = (new_entry['d_ping'] - self.mean) / (self.n_samples)
					self.mean += delta_mean
					if self.debug:
						print("\n** New entry **\n\tDelta_ICMP_inechos: " + str(new_entry['d_ping']))
						print("\tCurrent mean: " + str(self.mean))
					self.ring_the_alarm(self.under_attack(new_entry['d_ping'], self.mean))
			time.sleep(5)
	
	def under_attack(self, ping_sample, current_mean):
		if self.debug:
			print("\tCurrent prediction: " + str(self.svm_inst.predict([[ping_sample, current_mean]])[0]))
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
		if self.client.write_points(data_json) and self.debug:
			print('\t[OK] Data was correctly sent to InfluxDB :)\n')

	# --- Aux Methods --- #	
	def get_ddos_json_body(self, boolean):
		return [{'measurement': 'ddos', 'fields': {'value': boolean}, 'tags': {'host': 'Ryu_Controller'}, 'time': self.get_datetime()}]
	
	def get_datetime(self):
		return (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ')

def ctrl_c_handler(s, f):
	print("\b\bShutting down MR. SVM... Bye!")
	exit(0)
 
if __name__ == "__main__":
	signal.signal(signal.SIGINT, ctrl_c_handler)
	ai_bot = gar_py(db_host = '10.0.123.3', dbg = True)
	# Load up the AI and start rocking!
	ai_bot.work_time()
