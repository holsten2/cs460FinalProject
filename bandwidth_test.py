#!/usr/bin/env python3

import sys
from optparse import OptionParser #For passing args
from subprocess import * #Making system calls
from time import *
import json
import os

import numpy as np
import matplotlib.pyplot as plt


#TODO:
#MAKE RESULTS.JSON ON CONFIG ==> "[]"

def main():
	# if(len(sys.argv) < 2):
	# 	print("PASS PARAMATER PLS")
	# 	sys.exit(0)

	parser = OptionParser()
	parser.add_option("-d", "--duration", dest="duration",
                  help="Duration of bandwidth test in hours", default=0)
	parser.add_option("-f", "--freq",dest="freq",
                  help="Frequency of tests in minutes",  default=10)
	parser.add_option("-p", "--path", dest="pathname",
                  help="write report to relative PATH", default=".")

	

	(options, args) = parser.parse_args()






	#set args
	duration = float(options.duration)
	freq = float(options.freq)
	path = options.pathname


	#get number of runs
	number_of_runs = 0
	curr_run = 0
	if duration == 0:
		number_of_runs = 1
	else:
		number_of_runs = int((duration * 60) / freq)


	output_file = path + "/current_test"
	args1 = "--bytes"
	args2 = "--simple"

	# process_worker = os.fork()
	# if process_worker != 0:
	# 	print("Executing scan on PID: ", process_worker)
	# 	finish_time = time() + (duration * 60 * 60)
	# 	print_time = strftime('%H:%M, %Y-%m-%d', localtime(finish_time))
	# 	print("Approximate time scan will finish: ", print_time)
	# 	exit(0)

	print("Executing scan on PID: ", os.getpid())
	finish_time = time() + (duration * 60 * 60)
	print_time = strftime('%H:%M, %Y-%m-%d', localtime(finish_time))
	print("Approximate time scan will finish: ", print_time)

	while(curr_run < number_of_runs):
		before_time = time()

		# Run test command and place into output file
		test_cmd = ["speedtest-cli", args1, args2]
		with open(output_file, "w") as outfile:
			call(test_cmd, stdout=outfile)


		#Open correct files 
		curr_file = open(output_file, "r")
		result_file = open("results.json", "rb+")

		curr_input = curr_file.read()
		
		#Extract the correct information
		timestamp = strftime("%m/%d/%y::%H:%M:%S",localtime())
		curr_ping = curr_input.split("Ping: ")[1].split("Download")[0].split(" ms")[0]
		curr_down = curr_input.split("Download: ")[1].split("Upload")[0].split(" Mbyte/s")[0]
		curr_up = curr_input.split("Upload: ")[1].split(" Mbyte/s")[0]

		#Create Object
		curr_obj = {
			"time" : timestamp,
			"ping" : curr_ping,
			"down" : curr_down,
			"curr_up" : curr_up 
		}

		
		#If first run initialize the file
		if curr_run == 0:
			curr_write = '[\n' + json.dumps(curr_obj, sort_keys=True, indent=4, separators=(',', ': ')) +'\n]'
			# result_file.write(bytes(curr_write, 'UTF-8'))
			result_file.write(curr_write)



		#If not first run add on
		else:
			result_file.seek(-2, 2)
			curr_write = ',\n' + json.dumps(curr_obj, sort_keys=True, indent=4, separators=(',', ': ')) +'\n]'
			# result_file.write(bytes(curr_write, 'UTF-8'))
			result_file.write(curr_write)


		after_time = time()

		elapsed_time = after_time - before_time
		wait_time = 60 * freq - elapsed_time
		
		curr_run += 1
		
		# print("sleeping for: ", wait_time)
		print(elapsed_time)
		if number_of_runs == curr_run:
			print(wait_time)
			sleep(wait_time)




	#Now we are done, print
	os.system('say "The scan has finished"')
		
	





if __name__ == "__main__":
	main()


























