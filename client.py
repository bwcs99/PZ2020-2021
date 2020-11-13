import socket

# Dane potrzebne do połączenia się z serwerem
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "DISCONNECT"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(ADDR)

#def prepare_initial_msg(nick):
#	return f"ADD_NEW_PLAYER:{nick}"

# Funkcja służąca do odbierania wiadomości z serwera
def rec_msg():
	msg_len = sock.recv(HEADER).decode(FORMAT)
	if msg_len:
		incoming_msg = sock.recv(int(msg_len)).decode(FORMAT)
	return incoming_msg

# Funkcja służąca do wysyłania żądań na serwer
def send_msg(msg):
	message = msg.encode(FORMAT)
	message_length = len(message)
	send_length = str(message_length).encode(FORMAT)
	send_length += b' '*(HEADER - len(send_length))
	sock.send(send_length)
	sock.send(message)
	print("THE MESSAGE HAS BEEN SENT")
	#print(sock.recv(2048).decode(FORMAT))
	response = rec_msg()
	if response:
		#print("TU")
		print(response)

# Funkcja służąca do łączenia się z serwerem + obsługa błędów
def connect_to_server():
	try:
		print("TYPE YOUR NICK BELOW: ")
		nick = str(input())
		send_msg(nick)
		while True:
			msg_to_send = str(input())
			send_msg(msg_to_send)
			if msg_to_send == DISCONNECT_MESSAGE:
				break
	except KeyboardInterrupt:
		print("CLIENT PROCESS TERMINATED")

connect_to_server() 


	
	