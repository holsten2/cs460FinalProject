#!/usr/bin/python3
from ProtocolParser import *
import time
import socket
import struct
import threading
import sys

PROTOCOLS_SPEC_FILE = '../protocols.spec'

TCP_IP 		= '0.0.0.0'
TCP_PORT 	= 1235
LENGTH_SIZE = 4

#TODO: ADD RANDOMIZED BITS
class Server:

	def __init__(self):
		pass

	def listen(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((TCP_IP, TCP_PORT))
		self.socket.listen(1)

		# conn, addr = self.socket.accept()
		# self.handle_protocol_request(conn, addr);
		
		while True:
			conn, addr = self.socket.accept()
			handler = threading.Thread(target=self.handle_protocol_request, args=(conn, addr) )
			handler.daemon = False
			handler.start()
		conn.close()

	def find_response(self, current_index):

		for index in range(current_index, len(self.commands)):
			if self.commands[index][0] == 'server':
				if self.randomize_bytes:
					return urandom(len(self.commands[index][1]))
				else:
					return self.commands[index][1]

	def handle_protocol_request(self, conn, addr):
		data = conn.recv(LENGTH_SIZE)
		if len(data) == 0:
			return
		msg_len = struct.unpack("I", data)[0]
		msg = conn.recv(msg_len)

		print("Received protocol request to use ", msg.decode('utf-8'))
		self.parser = ProtocolParser(msg.decode('utf-8'))
		self.commands = self.parser.parse_commands_from_file(PROTOCOLS_SPEC_FILE)

		self.randomize_bytes = bool(struct.unpack("?", conn.recv(1))[0] )

		response = "OK"
		conn.send(struct.pack("s", response.encode('utf-8')))
		self.handle_connection(conn, addr)
		return


	def handle_connection(self, conn, addr):
		index = 1
		while True:
			
			data = conn.recv(LENGTH_SIZE)
			if len(data) == 0:
				return
			msg_len = struct.unpack("I", data)[0]
			msg = conn.recv(msg_len)

			print("Received request of size ", msg_len)
			
			response = self.find_response(index)
			conn.send(struct.pack( "I", len(response) ))
			conn.send(response)

			print("Replying with response of size ", len(response))

			index += 2



c = Server();
c.listen()

