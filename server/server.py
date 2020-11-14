import socket
import threading
from player import Player

# Proszę nie ruszać zakomentowanego kodu. Będzie on zmieniany
# Dane potrzebne do wystartowania serwera. 
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "DISCONNECT"


# Listy do trzymania graczy, wątków i socketów
players = []
connections = []
threads = []


# Funkcja tworząca socket servera
def create_socket(addres):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(addres)
	return sock

# Potrzebne do tworzenia wysyłanego nagłówka
def header_generator(str_response):
	resp_len = str(len(str_response)).encode(FORMAT)
	resp_len += b' '*(HEADER - len(resp_len))
	return resp_len


#def broadcast(clients, curr_conn, response):
#	response1_length = header_generator(response[0])
#	response2_length = header_generator(response[1])
#	for client in clients:
#		if client != curr_conn:
#			print("TU1")
#			client.send(response2_length)
#			client.send(response[1])
#		else:
#			print("TU2")
#			client.send(response1_length)
#			client.send(response[0])

# Funkcja chroniąca przed zmienianiem ustawionego nicka
def check_for_collisions(player_list, name, flag):
	for player in player_list:
		if player.player_name == name:
			return True
	return False

# Służy do przetwarzania zapytań (na razie te dwa postawowe). : jest delimiterem (cf. funkcja "split()")
def parse_request(incoming_msg, addr):
	request = incoming_msg.split(":")
	response = []
	if request[0] == "ADD_NEW_PLAYER":
			if check_for_collisions(players, request[1], 'p'):
				response.append(f"YOUR NICK BELONGS TO ANOTHER PLAYER".encode(FORMAT))
				#response.append(f" ".encode(FORMAT))
			elif 
			else:
				new_player = Player(request[1])
				players.append(new_player)
				response.append(f"{request[1]}:YOU HAVE BEEN SUCCESSFULLY ADDED TO THE GAME".encode(FORMAT))
				#response.append(f"{request[1]} JOINED THE GAME".encode(FORMAT))
	elif request[0] == "CHOOSE_CIVILISATION":
		for player in players:
			if player.player_name == request[1]:
				player.set_civilisation_type = request[2]
		response.append(f"{request[1]}: YOU HAVE CHOSEN: {request[2]}".encode(FORMAT))
		#response.append(f"{request[1]} CHOSEN TYPE: {request[2]}")
	else:
		response.append(f"UNKNOWN OPTION".encode(FORMAT))
		#response.append(f" ")
	return response
		
# Służy do obsługi klientów
def connection_handler(conn, addr):
	print(f"NEW CONNECTION FROM {addr} ")
	connected = True
	while connected:
		msg_leng = conn.recv(HEADER).decode(FORMAT)
		if msg_leng:
			msg_leng = int(msg_leng)
			incoming_message = conn.recv(msg_leng).decode(FORMAT)
			print(f"RECEIVED NEW MESSAGE: {incoming_message} from {addr}")
			if incoming_message == DISCONNECT_MESSAGE:
				connected = False
			response = parse_request(incoming_message, addr)
			response_length = header_generator(response[0])
			conn.send(response_length)
			conn.send(response[0])
	conn.close()


# Funkcja akceptująca przychodzące połączenie i tworząca oddzielny wątek dla każdego klienta
def start_connection(server_socket):
	try:
		server_socket.listen()
		print(f"IM HERE: {HOST} {PORT}")
		while True:
			conn, addr = server_socket.accept()
			connections.append(conn)
			new_thread = threading.Thread(target=connection_handler, args=(conn, addr))
			threads.append(new_thread)
			new_thread.start()
			print(f"N_O ACTIVE CONNECTIONS: {threading.activeCount()-1}")
	except KeyboardInterrupt:
		for thread in threads:
			thread.join()
		print("SERVER PROCESS TERMINATED")
						

print("SERVER IS STARTING")

server = create_socket(ADDR)

start_connection(server)