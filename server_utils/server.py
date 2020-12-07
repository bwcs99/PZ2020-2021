import socket
import threading
from random import randint

from .player import Player

# Dane potrzebne do wystartowania serwera.
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 200
DISCONNECT_MESSAGE = "DISCONNECT"
default_game_time = 30

#dummy1 = Player('edzia', 'red')
#dummy2 = Player('marcel', 'pink')
#dummy1.civilisation_type = 'zgredki'
#dummy2.civilisation_type = 'antysczepionkowcy'
#dummy1.city_list = ['Fangorn', 'Moskwa', 'Berlin']
#dummy2.city_list = ['Rumunia', 'Peja', 'Rychu', 'Bieda']


class Server:

    def __init__(self, terrain_map):
        """
        :param terrain_map: A 2D list of integer values representing tile types on the map.
        """
        self.map_to_send = terrain_map
        self.players = []
        self.connections = []
        self.threads = []
        self.colours = ['pink', 'red', 'purple', 'yellow', 'green', 'brown', 'blue', 'orange', 'gray']
        self.civilizations = ["zgredki", "elfy", "40-letnie-panny", "antysczepionkowcy"]
        self.current_player = 0  # index in self.players that indicates who is active
        self.finish = False
        self.server_sock = self.create_socket(ADDR)
        self.start_connection(self.server_sock)

 #   def custom_timer(self, time):
 #       sleep(time*60)
 #       finish = True

    def create_socket(self, address):
        """
        Initializes the server's socket.
        :param address: the server's address that the sock will be bound to
        :return: the initialized socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)
        return sock

    def header_generator(self, str_response):
        """
        Generates a proper header for a message.
        :param str_response: a message for which the header will be generated
        :return: the header containing the message length
        """
        resp_len = str(len(str_response)).encode(FORMAT)
        resp_len += b' ' * (HEADER - len(resp_len))
        return resp_len

    ''' Funkcja obliczająca ranking na podstawie liczby przyznanych punktów '''
    def compute_rank(self, player_list):
        player_list.sort(key=lambda player: player.scores, reverse=True)
        rank = 1
        player_list[0].rank = rank
        rank_list = []
        for i in range(1, len(player_list)):
            if player_list[i-1].scores == player_list[i].scores:
                player_list[i].rank = rank
                continue
            else:
                rank += 1
                player_list[i].rank = rank
        for player in player_list:
            rank_list.append((player.player_name, player.rank))
        return rank_list
        
    def parse_request(self, incoming_msg, addr):
        """
        Used to generate a response/broadcast reacting to a clients message. A response is only sent to the original
        caller, whereas a broadcast is sent to every client that's currently connected.
        :param incoming_msg: the message that's being responded to
        :param addr: the address of the client whose call is being responded to
        :return: a tuple of response (a list of messages that will be sent to the og caller) and broadcast (a single
        message that will be sent to everybody)
        """
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
                # broadcast = f"NEW PLAYER".encode(FORMAT)

        elif request[0] == "CHOOSE_CIVILISATION":
            if len(self.civilizations) != 0:
                for player in self.players:
                    if player.player_name == request[1]:
                        # idx = self.civilizations.index(request[1])
                        self.civilizations.remove(request[2])
                        player.set_civilisation_type(request[2])
                        broadcast = f"NEW_PLAYER:{player.player_name}:{player.civilisation_type}:{player.player_colour}"
                        broadcast = broadcast.encode(FORMAT)
            response.append(f"{request[1]} CHOSEN TYPE: {request[2]}".encode(FORMAT))

        elif request[0] == "LIST_PLAYERS":
            player_list = []
            for player in self.players:
                player_string = player.player_name
                player_string += ':'
                player_string += player.civilisation_type
                player_string += ':'
                player_string += player.player_colour
                player_list.append(player_string)
            response.append(str(player_list).encode(FORMAT))

        elif request[0] == "LIST_CIVILIZATIONS":
            civilizations_in_string = str(self.civilizations)
            response.append(f"{civilizations_in_string}".encode(FORMAT))

        elif request[0] == "SHOW_MAP":
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

        elif request[0] == "EXIT_LOBBY":
            # TODO rethink Client.only_send() being used here
            # response.append(f"ALL_EXIT_LOBBY".encode(FORMAT))
            broadcast = f"FINISH:::".encode(FORMAT)

        elif request[0] == "MORE_MONEY":
          #  print('W more_money')
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            wanted.treasury += int(request[2])
          #  print(wanted.treasury)
        
        elif request[0] == "LESS_MONEY":
        #   print('W less_money')
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            wanted.treasury -= int(request[2])
        #    print(wanted.treasury)

        elif request[0] == "GET_TREASURY":
     #       print('W get_treasury_state')
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
      #      print("Stan skarbca: ", wanted.treasury)
            response.append(f"{wanted.treasury}".encode(FORMAT)) 

        elif request[0] == "QUIT_GAME":
        #    print('W quit_game')
        #    print(self.connections)
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            self.players.remove(wanted)
            idx = self.players.index(wanted)
            self.connections[idx].close()
            self.connections.pop(idx)
            self.threads[idx].join()
            self.threads.pop(idx)
        #   print(self.connections)

        elif request[0] == "ADD_SCORES":
           # print('W add_scores')
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            wanted.scores += int(request[2])
           # print('Punkty: ', wanted.scores)

        elif request[0] == "END_GAME":
            ranking = self.compute_rank(self.players)
         #   print(ranking)
            broadcast = str(self.compute_rank(self.players)).encode(FORMAT)
         #   print(broadcast)

        elif request[0] == "CHANGE_MAP":
         #   print('W change map')
         #   print(request[2])
            broadcast = request[2].encode(FORMAT)
        
        elif request[0] == "ADD_CITY":
          #  print('W add_city')
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            wanted.city_list.append(request[2])
          #  print('Lista: ', wanted.city_list)

        elif request[0] == "GIVE_CITIES":
          #  print('W give_cities')
            wanted1 = next((player for player in self.players if player.player_name == request[1]), None)
            wanted2 = next((player for player in self.players if player.player_name == request[2]), None)
            cities = eval(request[3])
          #  print(cities)
          #  print('Listy gracza 1: ', wanted1.city_list)
          #  print('Listy gracza 2: ', wanted2.city_list)
            for city in cities:
                wanted2.city_list.append(city)
                wanted1.city_list.remove(city)
          #  print("Pierwszy gracz: ", wanted1.city_list)
          #  print('Drugi gracz: ', wanted2.city_list)
        
        elif request[0] == "LIST_CITIES":
          #  print('W list_cities')
            temp_list = []
            for player in self.players:
                temp_list.append((player.player_name, player.city_list))
            temp_list_to_str = str(temp_list)
          #  print(temp_list_to_str)
            response.append(temp_list_to_str.encode(FORMAT))

        else:
            response.append(f"UNKNOWN OPTION".encode(FORMAT))
        return response, broadcast

    def connection_handler(self, conn, addr):
        """
        Oversees client-server communication. Is being run in its separate thread for each client.
        :param conn: socket object used to send and receive data to the client
        :param addr: client's address
        """
        print(f"NEW CONNECTION FROM {addr} ")
        connected = True
        while connected:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                incoming_message = conn.recv(msg_len).decode(FORMAT)
                print(f"RECEIVED NEW MESSAGE: {incoming_message} from {addr}")
                if incoming_message == DISCONNECT_MESSAGE or finish:
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

    def start_connection(self, server_socket):
        """
        Accepts a new client connection and creates a thread for handling it.
        """
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
