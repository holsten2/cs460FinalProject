from ProtocolParser import *
import time
import socket
import struct
import sys
import json

PROTOCOLS_SPEC_FILE = '../protocols.spec'

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1235
LENGTH_SIZE = 4
BUFFER_SIZE = 1048576

class Client:

	def __init__(self, protocol):
		if len(sys.argv) < 2:
			print ("Usage: Client.py protocol")
			sys.exit(0)
		self.parser = ProtocolParser(protocol)
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE)

	def send_command(self, command, index):
		command_length = len(command[1])
		self.connection.send(struct.pack("I", command_length))
		self.connection.send(command[1])
		print("Sending request of size ", command_length)
		
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

	def replay_commands(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((SERVER_IP, SERVER_PORT))
		total_size = 0
		total_time = 0.0
		for index, command in enumerate(self.commands):
			if(command[0] == 'client'):
				curr_stats = self.send_command(command, index)
				total_size += curr_stats[0]
				total_time += curr_stats[1]
		self.connection.close()

		return (total_size, total_time)



c = Client(sys.argv[1]);

stats = c.replay_commands()

total_size = stats[0]
total_time = stats[1]

kbps = ( (stats[0] / 1000.0) / total_time)

print ( json.dumps({"protocol": sys.argv[1], "total_time": total_time, "total_size": total_size, "KB/S": kbps}))