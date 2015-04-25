from ProtocolParser import *
import time
import socket

PROTOCOLS_SPEC_FILE = '../protocols.spec'

TCP_IP 		= '0.0.0.0'
TCP_PORT 	= 1235
LENGTH_SIZE = 64

class Server:

	def __init__(self):
		self.parser = ProtocolParser('BitTorrent');
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE);

	def replay_commands(self):
		for command in self.commands:
			if(command[0] == 'server'):
				print("Performing server command")
			else:
				time.sleep(3)
	def listen(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((TCP_IP, TCP_PORT))
		self.socket.listen(1)
		conn, addr = self.socket.accept()
		data = conn.recv(LENGTH_SIZE)
		print ("received data:", data.decode("utf-8", "strict"))
		#conn.send(data)  # echo
		conn.close()


c = Server();
c.listen()

