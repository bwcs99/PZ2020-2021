import socket

# Dane potrzebne do połączenia się z serwerem
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "DISCONNECT"

class Client:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#def prepare_initial_msg(nick):
	#	return f"ADD_NEW_PLAYER:{nick}"

	# Funkcja służąca do odbierania wiadomości z serwera
	def rec_msg(self):
		msg_len = self.sock.recv(HEADER).decode(FORMAT)
		if msg_len:
			incoming_msg = self.sock.recv(int(msg_len)).decode(FORMAT)
		return incoming_msg

	# Funkcja służąca do wysyłania żądań na serwer
	def send_msg(self, msg):
		message = msg.encode(FORMAT)
		message_length = len(message)
		send_length = str(message_length).encode(FORMAT)
		send_length += b' '*(HEADER - len(send_length))
		self.sock.send(send_length)
		self.sock.send(message)
		#print("THE MESSAGE HAS BEEN SENT")
		#print(sock.recv(2048).decode(FORMAT))
		response = self.rec_msg()
		if response:
			#print("TU")
			print(response)

	# Funkcja służąca do łączenia się z serwerem + obsługa błędów
	def connect_to_server(self):
		try:
			print("TYPE YOUR NICK BELOW: ")
			nick = str(input())
			self.send_msg(nick)
			while True:
				msg_to_send = str(input())
				self.send_msg(msg_to_send)
				if msg_to_send == DISCONNECT_MESSAGE:
					break
		except KeyboardInterrupt:
			print("CLIENT PROCESS TERMINATED")

	def connect(self):
		self.sock.connect(ADDR)

	def disconnect(self):
		self.send_msg(DISCONNECT_MESSAGE)
		self.sock.close()

# connect_to_server()


	
	