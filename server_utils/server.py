import socket
import threading
from player import Player
from map_generation import generate_map
from random import randint

# Proszę nie ruszać zakomentowanego kodu. Będzie on zmieniany
# Dane potrzebne do wystartowania serwera. 
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 200
DISCONNECT_MESSAGE = "DISCONNECT"

"""	Gabi:
	- potrzebuję konstruktor, która tworzy serwer. Z poziomu GUI mogę już dostarczyć do konstruktora:
	    1. mapę gry, w postaci macierzy i obrazka.
	    2. nick i cywilzacje hosta.
	    uwaga: niech będzie pole z nazwami cywilizacji, niech będą zahardkodowane ["zgredki", "elfy", "40-letnie-panny", "antysczepionkowcy"], takie same jak w oknie CivCombo z nick_civ_window.py
	- potrzebuję odpowiednie zachowanie z metodami z clienta
    - potrzebuję aby po dodaniu nowego gracza wysyłany był komunikat do wszytskich klientów o dodaniu nowego gracza, co pozwoli odświeżyć tabelę w lobby_window.
"""


class Server:

    def __init__(self, param1, param2):
        self.map_to_send = generate_map(param1, param2, [1, 8, 28, 6])
        print(self.map_to_send)
        self.players = []
        self.connections = []
        self.threads = []
        self.colours = ['pink', 'red', 'purple', 'yellow', 'green', 'brown', 'blue', 'orange', 'grey']

    # Funkcja tworząca socket servera
    def create_socket(self, addres):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addres)
        return sock

    # Potrzebne do tworzenia wysyłanego nagłówka
    def header_generator(self, str_response):
        resp_len = str(len(str_response)).encode(FORMAT)
        resp_len += b' ' * (HEADER - len(resp_len))
        return resp_len

    #	def convert_array(self, arr, p1, p2):
    #		str_list = ''
    #		for i in range(0, p1):
    #			for j in range(0, p2):
    #				alnum = str(arr[i][j])
    #				str_list += alnum
    #				if j == p2-1 :
    #					str_list += 'e'
    #		print(str_list)
    #		return str_list

    def parse_request(self, incoming_msg, addr):
        request = incoming_msg.split(":")
        response = []
        if request[0] == "ADD_NEW_PLAYER":
            if len(self.colours) != 0:
                print("W dodawaniu nowego gracza")
                idx = randint(0, len(self.colours) - 1)
                col = self.colours[idx]
                self.colours.remove(col)
                new_player = Player(request[1], col)
                self.players.append(new_player)
                response.append(f"{request[1]}:YOU HAVE BEEN SUCCESSFULLY ADDED TO THE GAME".encode(FORMAT))
        # response.append(f"{request[1]} JOINED THE GAME".encode(FORMAT))
        elif request[0] == "CHOOSE_CIVILISATION":
            print("W ustawianiu typu cywilizacji")
            for player in self.players:
                if player.player_name == request[1]:
                    player.set_civilisation_type(request[2])
            #	response.append(f"{request[1]}: YOU HAVE CHOSEN: {request[2]}".encode(FORMAT)) # tu zmiana
            enc_map = str(self.map_to_send)
            #	print(enc_map)
            response.append(enc_map.encode(FORMAT))  # tu zmiana
        # tu zmiana
        # response.append(f"{request[1]} CHOSEN TYPE: {request[2]}")
        elif request[0] == "LIST_PLAYERS":
            print("W listowaniu graczy")
            lis = ''
            for player in self.players:
                lis += player.player_name
                lis += ' '
                print(player.civilisation_type)
                lis += player.civilisation_type
                lis += ' '
                lis += player.player_colour
                lis += ' '
            response.append(lis.encode(FORMAT))
        else:
            response.append(f"UNKNOWN OPTION".encode(FORMAT))
        # response.append(f" ")
        return response

    # Służy do obsługi klientów
    def connection_handler(self, conn, addr):
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
                response = self.parse_request(incoming_message, addr)
                if len(response) != 0:
                    response_length = self.header_generator(response[0])
                    conn.send(response_length)
                    conn.send(response[0])
        conn.close()

    # Funkcja akceptująca przychodzące połączenie i tworząca oddzielny wątek dla każdego klienta
    def start_connection(self, server_socket):
        try:
            server_socket.listen()
            print(f"IM HERE: {HOST} {PORT}")
            while True:
                conn, addr = server_socket.accept()
                self.connections.append(conn)
                new_thread = threading.Thread(target=self.connection_handler, args=(conn, addr))
                self.threads.append(new_thread)
                new_thread.start()
                print(f"N_O ACTIVE CONNECTIONS: {threading.activeCount() - 1}")
        except KeyboardInterrupt:
            for thread in self.threads:
                thread.join()
            print("SERVER PROCESS TERMINATED")


print("SERVER IS STARTING")

server_obj = Server(50, 50)

server = server_obj.create_socket(ADDR)

server_obj.start_connection(server)
