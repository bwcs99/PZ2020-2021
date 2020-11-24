import socket
import threading
from random import randint
from player import Player

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
        # print(self.map_to_send)
        self.players = []
        self.current_player = 0  # index
        self.connections = []
        self.threads = []
        self.colours = ['pink', 'red', 'purple', 'yellow', 'green', 'brown', 'blue', 'orange', 'grey']
        self.civilizations = ["zgredki", "elfy", "40-letnie-panny", "antysczepionkowcy"]

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
        if request[0] == "ADD_NEW_PLAYER":
            if len(self.colours) != 0:
                print("W dodawaniu nowego gracza")
                idx = randint(0, len(self.colours) - 1)
                col = self.colours[idx]
                self.colours.remove(col)
                new_player = Player(request[1], col)
                new_player.active = True
                self.players.append(new_player)
                response.append(f"{request[1]}:YOU HAVE BEEN SUCCESSFULLY ADDED TO THE GAME".encode(FORMAT))
                for player in self.players:
                    player.message_queue.append(f"NEW PLAYER".encode(FORMAT))
        elif request[0] == "CHOOSE_CIVILISATION":
            print("W ustawianiu typu cywilizacji")
            if len(self.civilizations) != 0:
                for player in self.players:
                    if player.player_name == request[1]:
                        # idx = self.civilizations.index(request[1])
                        self.civilizations.remove(request[1])
                        player.set_civilisation_type(request[2])
            response.append(f"{request[1]} CHOSEN TYPE: {request[2]}".encode(FORMAT))
        elif request[0] == "LIST_PLAYERS":
            print("W listowaniu graczy")
            to_send = []
            for player in self.players:
                help = [player.player_name, player.civilisation_type, player.player_colour]
                to_send.append(help)
            enc_to_send = str(to_send)
            response.append(enc_to_send.encode(FORMAT))
        elif request[0] == "LIST_CIVILIZATIONS":
            enc_lis = str(self.civilizations)
            response.append(enc_lis.encode(FORMAT))
        elif request[0] == "END_TURN":
            self.current_player += 1
            self.current_player %= len(self.players)
            t = ("TURN", self.players[self.current_player].player_name)
            enc_t = str(t)
            response.append(enc_t.encode(FORMAT))
        elif request[0] == "SHOW_MAP":
            enc_map = str(self.map_to_send)
            response.append(enc_map.encode(FORMAT))
        else:
            response.append(f"UNKNOWN OPTION".encode(FORMAT))
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
                for i in range(0, len(self.connections)):
                    if len(self.players[i].message_queue) != 0:
                        response_length = self.header_generator(self.players[i].message_queue[0])
                        self.connections[i].send(response_length)
                        self.connections[i].send(self.players[i].message_queue[0])
                        self.players[i].message_queue.clear()
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
