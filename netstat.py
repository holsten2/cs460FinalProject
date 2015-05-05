#!/usr/bin/env python

import sys
from optparse import OptionParser #For passing args
from subprocess import * #Making system calls
from time import *
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as pltd
from datetime import datetime



def plot_information(in_time, test_dir):
	result_file = open(test_dir + in_time + "results.json", "r")
	plot_data = result_file.read()

	json_object = json.loads(plot_data)
	date_list = []
	up_list = []
	down_list = []
	ping_list = []

	for i in range(0, len(json_object)):
		curr_time = str(json_object[i]['time'])
		currf_time = datetime.strptime(curr_time, "%m/%d/%y::%H:%M:%S")
		curr_up = float(json_object[i]['curr_up'])
		curr_down = float(json_object[i]['down'])
		curr_ping = float(json_object[i]['ping'])


		date_list.append(currf_time)
		up_list.append(curr_up)
		down_list.append(curr_down)
		ping_list.append(curr_ping)


	#UPLOAD 

	fig = plt.figure()
	ax = fig.add_subplot(111)

	# Configure x-ticks
	ax.set_xticks(date_list) # Tickmark + label at every plotted point
	ax.xaxis.set_major_formatter(pltd.DateFormatter('%d/%m/%Y %H:%M'))

	ax.plot_date(date_list, up_list, ls='-', marker='o')
	ax.set_title('Upload Speed')
	ax.set_ylabel('Upload Speeds (MB/s)')
	ax.set_xlabel('Time')
	ax.set_ylim(ymin=0)
	ax.grid(True)

	fig.autofmt_xdate(rotation=45)

	plt.gcf().subplots_adjust(bottom=0.25)
	plt.gcf().subplots_adjust(left=0.15)
	
	
	plt.savefig(test_dir + in_time + 'upload_speed.png')


	# DOWNLOAD

	fig = plt.figure()
	ax = fig.add_subplot(111)

	# Configure x-ticks
	ax.set_xticks(date_list) # Tickmark + label at every plotted point
	ax.xaxis.set_major_formatter(pltd.DateFormatter('%d/%m/%Y %H:%M'))

	ax.plot_date(date_list, down_list, ls='-', marker='o')
	ax.set_title('Download Speed')
	ax.set_ylabel('Download Speeds (MB/s)')
	ax.set_xlabel('Time')
	ax.set_ylim(ymin=0)
	ax.grid(True)

	fig.autofmt_xdate(rotation=45)

	plt.gcf().subplots_adjust(bottom=0.25)
	plt.gcf().subplots_adjust(left=0.15)
	
	plt.savefig(test_dir + in_time + 'download_speed.png')


	# PING

	fig = plt.figure()
	ax = fig.add_subplot(111)

	# Configure x-ticks
	ax.set_xticks(date_list) # Tickmark + label at every plotted point
	ax.xaxis.set_major_formatter(pltd.DateFormatter('%d/%m/%Y %H:%M'))

	ax.plot_date(date_list, ping_list, ls='-', marker='o')
	ax.set_title('Ping')
	ax.set_ylabel('Pings (ms)')
	ax.set_xlabel('Time')
	ax.set_ylim(ymin=0)
	ax.grid(True)

	fig.autofmt_xdate(rotation=45)

	plt.gcf().subplots_adjust(bottom=0.25)
	plt.gcf().subplots_adjust(left=0.15)
	
	plt.savefig(test_dir + in_time + 'ping.png')






def main():

	parser = OptionParser()
	parser.add_option("-d", "--duration", dest="duration",
                  help="Duration of bandwidth test in hours", default=0)
	parser.add_option("-f", "--freq",dest="freq",
                  help="Frequency of tests in minutes",  default=0)



	(options, args) = parser.parse_args()

	#set args
	duration = float(options.duration)
	freq = float(options.freq)

	#get number of runs
	no_wait = False
	number_of_runs = 0
	curr_run = 0
	if duration == 0:
		number_of_runs = 1
	elif freq == 0:
		no_wait = True
		number_of_runs = -1
	else:
		number_of_runs = int((duration * 60) / freq)


	output_file = "current_test"
	args1 = "--bytes"
	args2 = "--simple"

	print "Executing scan on PID: " + str(os.getpid())
	finish_time = time() + (duration * 60 * 60)
	print_time = strftime('%H:%M, %Y-%m-%d', localtime(finish_time))
	print "Approximate time scan will finish: " + str(print_time)

	curr_time_string = strftime("%Y.%m.%d..%H.%M.",localtime())
	test_dir = curr_time_string + "test/"

	os.system("mkdir " + test_dir)
	os.system("touch " + test_dir + curr_time_string + "results.json")
	os.system("touch " + output_file)

	while((curr_run < number_of_runs) or no_wait):
		before_time = time()

		# Run test command and place into output file
		test_cmd = ["speedtest-cli", args1, args2]
		with open(output_file, "w") as outfile:
			call(test_cmd, stdout=outfile)

		
		#Open correct files
		curr_file = open(output_file, "r")
		result_file = open(test_dir + curr_time_string + "results.json", "rb+")

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


		result_file.close()
		plot_information(curr_time_string, test_dir)

		after_time = time()

		elapsed_time = after_time - before_time
		wait_time = 60 * freq - elapsed_time
		curr_run += 1

	

		# print("sleeping for: ", wait_time)

		print("ELAPSED TIME = " + str(elapsed_time))
		if no_wait:
			print("SLEEPING FOR = 0") 
		elif number_of_runs != curr_run:
			print("SLEEPING FOR = " + str(wait_time))
			sleep(wait_time)

		print("")
		if after_time > finish_time:
			break

	#Now we are done, print
	os.system("rm " + output_file)
	os.system('say "The scan has finished"')












if __name__ == "__main__":
	main()
