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

	
	def work_time():
		# Classify the traffic calling any needed methods
		while True:
			pass
	
	def get_data():
		# Get data from InfluxDB
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
	
	# Unit test
	print(ai_bot.get_datetime())
	print(ai_bot.get_ddos_json_body(True))
	ai_bot.ring_the_alarm(True)
		
	ai_bot.work_time()
