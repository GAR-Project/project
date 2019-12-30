from influxdb import InfluxDBClient
import datetime

class gar_py:
	def __init__(self, host='localhost', port=8086):
		""" Builder n.n """
		
		# Include any config variables you may need
		self.n_samples, self.traffic_mean, self.traffic_sensity = 0, 0, 0
		self.host = host
		self.port = port
		self.dbname = 'telegraf'
		self.client = InfluxDBClient(host, port, 'root', 'root', self.dbname)
		
		# Comillas triples ya que si o si tenemos que usar comillas simples para taggear la etiqueta. 
		self.query = """select bytes_sent from net where interface = 's1-eth1';"""
		
		# Ejemplos de querys:
		# select icmp_inmsgs, icmp_outmsgs from net
		# select * from net where time >= '2019-12-31T00:00:00Z' and time < '2019-12-30T16:00:00Z'
		
	def work_time():
		# Classify the traffic calling any needed methods
		while True:
			pass
	

	def get_data(self, pet):
		# Get data from InfluxDB
		read_traffic = self.client.query(pet)
		return read_traffic

	def ring_the_alarm(self, boolean_value):
		# Ring the alarm by writing to InfluxDB
		data_json = self.get_ddos_json_body(boolean_value)
		if self.client.write_points(data_json):
			print('[OK] Data was correctly sent to InfluxDB')
		return


	# --- Aux Methods --- #	
	
	def get_ddos_json_body(self, boolean):
		return [{'measurement': 'ddos', 'fields': {'value': boolean }, 'tags': {'host': 'Ryu_Controller'}, 'time': self.get_datetime() }]
	
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
	
	# Init
	ai_bot.work_time()
