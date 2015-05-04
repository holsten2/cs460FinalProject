#!/usr/bin/python3
from ProtocolParser import *
import time
import socket
import struct
import sys
import json
from optparse import OptionParser
import os
from scipy import stats 

PROTOCOLS_SPEC_FILE = '../protocols.spec'

SERVER_IP = '52.11.186.220'
SERVER_PORT = 1235
LENGTH_SIZE = 4
BUFFER_SIZE = 1048576
P_VALUE_THRESHOLD = 0.05

class Client:

	def __init__(self, protocol):
		if len(sys.argv) < 2:
			print ("Usage: Client.py protocol")
			sys.exit(0)
		self.protocol = protocol
		self.parser = ProtocolParser(protocol)
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE)

	def send_command(self, command, index):
		command_length = len(command)
		print("Sending request of size ", command_length)
		self.connection.send(struct.pack("I", command_length))
		self.connection.send(command)
		
		
		response_size_buf = self.connection.recv(LENGTH_SIZE)
		response_size = struct.unpack("I", response_size_buf)[0]

		response = b''
		timeBefore = round(time.time()*1000)
		while len(response) != response_size:
			response += self.connection.recv(BUFFER_SIZE)
		timeAfter = round(time.time()*1000)
		timeSeconds = (timeAfter-timeBefore) / 1000.0
		if len(self.commands[index+1][1]) == len(response):
			print ("Received valid response of size ", len(response))
		else:
			print ("Received corrupted response of size ", len(response))
		return (len(response), timeSeconds)

	def replay_commands(self, randomize):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((SERVER_IP, SERVER_PORT))

		if randomize:
			print("Sending protocol request to server to use random bytes to compare with ", self.protocol)
		else:
			print("Sending protocol request to server to use ", self.protocol)

		self.connection.send(struct.pack("I", len(self.protocol.encode('utf-8'))) )
		self.connection.send(self.protocol.encode('utf-8'))

		self.connection.send(struct.pack("?", randomize))

		protocol_response = self.connection.recv(2)
		
		if protocol_response.decode('utf-8') == "OK":
			print ("Server acknowledged protocol request")


		total_size = 0
		total_time = 0.0
		for index, command in enumerate(self.commands):
			if(command[0] == 'client'):
				if(randomize):
					curr_stats = self.send_command( os.urandom(len(command[1]) ), index)
				else:	
					curr_stats = self.send_command(command[1], index)
				total_size += curr_stats[0]
				total_time += curr_stats[1]
		self.connection.close()

		return (total_size, total_time)

def kilobytes_per_second(num_bytes, seconds):
	return ((num_bytes / 1000.0) / seconds)	

def average(list):
	return sum(list)/float(len(list))

def testProtocol(randomize):
	bandwidth = []
	for i in range(0,int(options.trials)):
		c = Client(options.protocol);
		stats = c.replay_commands(randomize)
		bandwidth.append(kilobytes_per_second(stats[0], stats[1]))

	return bandwidth



parser = OptionParser()

parser.add_option("-p", "--protocol", dest="protocol",
                  help="Specify the protocol to use for the test")

parser.add_option("-n", "--trials", dest="trials", default="1",
                  help="Specify the number of trials to use for the test")
(options, args) = parser.parse_args()

protocol_sample = testProtocol(False)
control_sample = testProtocol(True)

average_protocol_bandwidth = average(protocol_sample)*8.0
average_random_bandwidth = average(control_sample)*8.0

print("Summary of testing:")
print ("Average bandwidth using "+options.protocol+": "+str(average_protocol_bandwidth)+" Kbit/s")
print ("Average bandwidth using random bytes: "+str(average_random_bandwidth)+" Kbit/s")

t_test_results = stats.ttest_ind(protocol_sample, control_sample, equal_var=False)
if( (t_test_results[0] < 0) and ( t_test_results[1] < P_VALUE_THRESHOLD) ):
	print ("Throttling detected. Difference in average bandwidth is statistically significant.")
else:
	print ("Throttling not detected. Difference in average bandwidth is not statistically significant.")


