import socket
import threading
from random import randint

from .player import Player

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

    def __init__(self, terrain_map):
        self.map_to_send = terrain_map
        print(self.map_to_send)
        # print(self.map_to_send)
        self.players = []
        self.connections = []
        self.threads = []
        self.colours = ['pink', 'red', 'purple', 'yellow', 'green', 'brown', 'blue', 'orange', 'grey']
        self.civilizations = ["zgredki", "elfy", "40-letnie-panny", "antysczepionkowcy"]
        self.current_player = 0  # index in self.players

        self.server_sock = self.create_socket(ADDR)
        self.start_connection(self.server_sock)

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

    def parse_request(self, incoming_msg, addr):
        request = incoming_msg.split(":")
        response = []
        broadcast = None
        if request[0] == "ADD_NEW_PLAYER":
            if len(self.colours) != 0:
                idx = randint(0, len(self.colours) - 1)
                col = self.colours[idx]
                self.colours.remove(col)
                new_player = Player(request[1], col)
                self.players.append(new_player)
                response.append(f"{request[1]}:YOU HAVE BEEN SUCCESSFULLY ADDED TO THE GAME".encode(FORMAT))
                broadcast = f"NEW PLAYER".encode(FORMAT)
        elif request[0] == "CHOOSE_CIVILISATION":
            if len(self.civilizations) != 0:
                for player in self.players:
                    if player.player_name == request[1]:
                        # idx = self.civilizations.index(request[1])
                        self.civilizations.remove(request[2])
                        player.set_civilisation_type(request[2])
            # response.append(f"{request[1]} CHOSEN TYPE: {request[2]}".encode(FORMAT))
        elif request[0] == "LIST_PLAYERS":
            lis = ''
            for player in self.players:
                print(player.player_name, player.civilisation_type, player.player_colour)
                lis += player.player_name
                lis += ':'
                lis += player.civilisation_type
                lis += ':'
                lis += player.player_colour
                print(lis)
            response.append(lis.encode(FORMAT))
            print(response)
        elif request[0] == "SHOW_MAP":
            print("W przesyłaniu mapy")
            map_in_string = str(self.map_to_send)
            response.append(f"{map_in_string}".encode(FORMAT))
        elif request[0] == "END_TURN":
            response.append(f"{request[1]}: YOU HAVE FINISHED YOUR TURN".encode(FORMAT))
            self.current_player += 1
            self.current_player %= len(self.players)
            t = ("TURN", self.players[self.current_player].player_name)
            broadcast = str(t).encode(FORMAT)
        elif request[0] == "START_GAME":
            response.append(f"{request[1]}: YOU HAVE STARTED THE GAME".encode(FORMAT))
            t = ("TURN", self.players[0].player_name)
            broadcast = str(t).encode(FORMAT)
        else:
            response.append(f"UNKNOWN OPTION".encode(FORMAT))
        # response.append(f" ")
        return response, broadcast

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
                response, broadcast = self.parse_request(incoming_message, addr)
                if len(response) != 0:
                    response_length = self.header_generator(response[0])
                    conn.send(response_length)
                    conn.send(response[0])
                if broadcast:
                    for c in self.connections:
                        length = self.header_generator(broadcast)
                        c.send(length)
                        c.send(broadcast)
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


# for testing
if __name__ == "__main__":
    server = Server([1, 2])