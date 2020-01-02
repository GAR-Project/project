import os, sys, time, datetime

# Global parameters
ERROR_BAD_ARGV_FROM_USER = '[pingGen] Error, incorrect arguments: '
INFO_INIT_1 = '[pingGen] Starting the pings on the given IP '
INFO_INIT_2 = '(Press CTRL+C to stop me)...'
INFO_STATS = '[pingGen] Quitting, showing stats:'
PKTS_CADENCE = 1
PKTS_LEN = 98
DATA_LEN = 1
DATA_STR = 'B'
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
		+ str(int(diff().total_seconds() * PKTS_CADENCE * PKTS_LEN / DATA_LEN)) + ' ' + DATA_STR + '\n')

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

	# Send those pings!
	os.system('ping -W 0.1 ' + sys.argv[1])	

	# Show the stats
	print('\n\n' + get_str_time() + INFO_STATS + '\n\n'+ stats())
