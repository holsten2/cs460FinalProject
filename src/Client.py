from ProtocolParser import *
import time
import socket
import struct

PROTOCOLS_SPEC_FILE = '../protocols.spec'

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1235
LENGTH_SIZE = 4
BUFFER_SIZE = 1024

class Client:

	def __init__(self):
		self.parser = ProtocolParser('BitTorrent')
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE)

	def send_command(self, command, index):
		command_length = len(command[1])
		self.connection.send(struct.pack("I", command_length))
		self.connection.send(command[1])
		print("Sending command of size ", command_length)
		
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
c.replay_commands()