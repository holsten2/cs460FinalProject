from ProtocolParser import *
import time
import socket
import struct
import sys

PROTOCOLS_SPEC_FILE = '../protocols.spec'

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1235
LENGTH_SIZE = 4
BUFFER_SIZE = 1024

class Client:

	def __init__(self):
		if len(sys.argv) < 2:
			print ("Usage: Client.py protocol")
			sys.exit(0)
		self.parser = ProtocolParser(sys.argv[1])
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE)

	def send_command(self, command, index):
		command_length = len(command[1])
		self.connection.send(struct.pack("I", command_length))
		self.connection.send(command[1])
		print("Sending request of size ", command_length)
		
		response_size_buf = self.connection.recv(LENGTH_SIZE)
		response_size = struct.unpack("I", response_size_buf)[0]

		response = b''
		while len(response) != response_size:
			response += self.connection.recv(BUFFER_SIZE)
		if len(self.commands[index+1][1]) == len(response):
			print ("Received valid response of size ", len(response))
		else:
			print ("Received corrupted response of size ", len(response))

	def replay_commands(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((SERVER_IP, SERVER_PORT))
		for index, command in enumerate(self.commands):
			if(command[0] == 'client'):
				self.send_command(command, index)
		self.connection.close()



c = Client();

timeBefore = round(time.time()*1000)
c.replay_commands()
timeAfter = round(time.time()*1000)

timeSeconds = (timeAfter-timeBefore) / 1000.0

print (timeSeconds, " seconds elapsed")