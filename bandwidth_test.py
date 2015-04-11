#!/usr/bin/env python3
import sys
from optparse import OptionParser #For passing args
from subprocess import * #Making system calls
from time import *
import json
import os


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
	duration = options.duration
	freq = options.freq
	path = options.pathname


	#get number of runs
	number_of_runs = 0
	curr_run = 0
	if duration == 0:
		number_of_runs = 1
	else:
		number_of_runs = (int(duration) * 60) / int(freq)

	output_file = path + "/current_test"
	args1 = "--bytes"
	args2 = "--simple"
	# args = "-h" 

	while(curr_run < number_of_runs):
		# Run test command and place into output file
		# test_cmd = ["speedtest-cli", args1, args2]
		# with open(output_file, "w") as outfile:
		# 	call(test_cmd, stdout=outfile)


		curr_file = open(output_file, "r")
		result_file = open("results.json", "r+")

		curr_input = curr_file.read()
		
		timestamp = strftime("%m/%d/%y::%H:%M:%S",localtime())
		curr_ping = curr_input.split("Ping: ")[1].split("Download")[0].split(" ms")[0]
		curr_down = curr_input.split("Download: ")[1].split("Upload")[0].split(" Mbyte/s")[0]
		curr_up = curr_input.split("Upload: ")[1].split(" Mbyte/s")[0]

		curr_obj = {
			"time" : timestamp,
			"ping" : curr_ping,
			"down" : curr_down,
			"curr_up" : curr_up 
		}

		


		if curr_run == 0:
			curr_results = []
			curr_results.append(curr_obj)


		else:
			curr_results = json.load(result_file)
			curr_results.append(curr_obj)

		write_obj = json.dumps(curr_results, indent=4)
		result_file.seek(0)
		result_file.write(write_obj)

		curr_run += 1
		
		# result_file.seek(-3, 2)
		# print(result_file.read())	
		# results = json.load(result_file)
		# results.append(curr_obj)

		# result_file.write((json.dumps(results, indent=4)))
		
	





if __name__ == "__main__":
	main()
