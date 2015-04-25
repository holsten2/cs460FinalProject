from ProtocolParser import *
import time
import socket

PROTOCOLS_SPEC_FILE = '../protocols.spec'

TCP_IP = '0.0.0.0'
TCP_PORT = 1234

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1235

class Client:

	def __init__(self):
		self.parser = ProtocolParser('BitTorrent');
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE);
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		self.connection.connect((SERVER_IP, SERVER_PORT))

	def replay_commands(self):
		self.connect()
		for command in self.commands:
			if(command[0] == 'client'):
				command_length = len(command[1])
				print(command_length)
				size = self.connection.send( str(command_length).encode('utf-8'))
				self.connection.send(command[1])

			else:
				time.sleep(3)


	def listen(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((TCP_IP, TCP_PORT))
		self.socket.listen(1)
		conn, addr = s.accept()
		print ('Connection address:', addr)
		while 1:
		    data = conn.recv(BUFFER_SIZE)
		    if not data: break
		    print ("received data:", data)
		    conn.send(data)  # echo
		conn.close()


c = Client();
c.replay_commands()