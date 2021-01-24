import socket
import threading
from random import randint

from map_generation.spread_players import spread_across_the_map
from server_utils.player import Player

# Dane potrzebne do wystartowania serwera.
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 200
DISCONNECT_MESSAGE = "DISCONNECT"
default_game_time = 30


def print_color(text):
    print("\u001b[36m" + text + "\u001b[0m")


class Server:

    def __init__(self, terrain_map):
        """
        :param terrain_map: A 2D list of integer values representing tile types on the map.
        """
        self.map_to_send = terrain_map
        self.players = []
        self.queue = []
        self.connections = dict()
        self.threads = []
        self.colours = ['BUBBLE_GUM', 'CHERRY', 'PURPLE', 'CORAL', 'MELLOW_APRICOT']
        self.civilizations = ["The Great Northern", "Kaediredameria", "Mixtec", "Kintsugi"]
        self.current_player = 0  # index in self.players that indicates who is active
        self.rank = 0  # for now
        self.started = False
        self.finish = False
        self.server_sock = self.create_socket(ADDR)
        self.start_connection(self.server_sock)

    def create_socket(self, address):
        """
        Initializes the server's socket.
        :param address: the server's address that the sock will be bound to
        :return: the initialized socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(1)
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
            if player_list[i - 1].scores == player_list[i].scores:
                player_list[i].rank = rank
                continue
            else:
                rank += 1
                player_list[i].rank = rank
        for player in player_list:
            rank_list.append((player.player_name, player.rank))
        return rank_list

    def get_particular_players(self, sender, receiver):
        """ zwraca listę graczy bez użytkowników o nickach sender (str) i receiver (str)
        return - lista graczy (typ Player) """
        res_list = []
        for player in self.players:
            if player.player_name == str(sender) or player.player_name == str(receiver):
                continue
            else:
                res_list.extend(player)
        return res_list

    # def inform_others(self, others_list, msg):
    #     """ dodaje określoną informacje (deklaracje wojny, zawarcie sojuszu itp.) do wiadomości innych użytkowników
    #     (nie będącymi stronami w danej sprawie). param1 - lista graczy (Player), param2 - wiadomość (str)"""
    #     for other in others_list:
    #         other.message_queue.extend([msg])

    ''' Udzielanie odpowiedzi każdemu z graczy'''

    def process_responses(self, response_list):
        """param1: lista odpowiedzi (str)"""
        for response in response_list:
            fields_values = response.split(":")
            receiver = next((player for player in self.players if player.player_name == fields_values[1]), None)
            receiver.message_queue.extend([response])
            others = self.get_particular_players(str(fields_values[1]), str(fields_values[2]))
            if "END_ALLIANCE" in response:
                msg = f'EAL_INFO:{fields_values[1]}:{fields_values[2]}'
                self.inform_others(others, msg)
            elif "ALLIANCE" in response and bool(fields_values[-1]):
                msg = f'ALC_INFO:{fields_values[1]}:{fields_values[2]}'
                self.inform_others(others, msg)
            elif "DECLARE_WAR" in response:
                msg = f'DCL_WAR_INFO:{fields_values[1]}:{fields_values[2]}'
                self.inform_others(others, msg)
            elif "GIVE_UP" in response:
                msg = f'GUP_INFO:{fields_values[1]}:{fields_values[2]}'
                self.inform_others(others, msg)
            elif "TRUCE" in response and bool(fields_values[-1]):
                msg = f'TRC_INFO:{fields_values[1]}:{fields_values[2]}'
                self.inform_others(others, msg)
            elif "BUY" in response and bool(fields_values[-1]):
                res_tuple = eval(fields_values[3])
                is_city = res_tuple[0]
                cords = res_tuple[1]
                if is_city:
                    msg = f'B_INFO:{fields_values[1]}:{fields_values[2]}:{cords}'
                    self.inform_others(others, msg)
                else:
                    continue

    def parse_request(self, incoming_msg, conn):
        """
        Used to generate a response/broadcast reacting to a clients message. A response is only sent to the original
        caller, whereas a broadcast is sent to every client that's currently connected.
        :param incoming_msg: the message that's being responded to
        :param conn: the connection with the client whose call is being responded to
        :return: a tuple of response (a list of messages that will be sent to the og caller) and broadcast (a list of
        messages that will be sent to everybody)
        """
        request = incoming_msg.split(":")
        response = []
        broadcast = []
        if request[0] == "ADD_NEW_PLAYER":
            if len(self.colours) != 0:
                idx = randint(0, len(self.colours) - 1)
                col = self.colours[idx]
                self.colours.remove(col)
                new_player = Player(request[1], col)
                self.players.append(new_player)
                self.connections[conn] = new_player
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
                        broadcast = [broadcast.encode(FORMAT)]
            response.append(f"{request[1]} CHOSEN TYPE: {request[2]}".encode(FORMAT))

        elif request[0] == "DISCONNECT":
            broadcast = [incoming_msg.encode(FORMAT)]
            player = self.connections[conn]
            player.rank = self.rank
            self.rank -= 1
            ind = self.queue.index(player)
            self.queue.pop(ind)
            if ind == self.current_player:
                ind = ind % len(self.queue)
                broadcast.append(f"TURN:{self.queue[ind].player_name}".encode(FORMAT))
            elif ind < self.current_player:
                self.current_player = (self.current_player - 1) % len(self.queue)
            self.connections.pop(conn)

        elif request[0] == "DEFEAT":
            broadcast = [incoming_msg.encode(FORMAT)]
            ind = None
            for i, player in enumerate(self.queue):
                if player.player_name == request[1]:
                    player.rank = self.rank
                    self.rank -= 1
                    ind = i
                    break
            if ind is not None:
                self.queue.pop(ind)
                if ind == self.current_player:
                    ind = ind % len(self.queue)
                    broadcast.append(f"TURN:{self.queue[ind].player_name}".encode(FORMAT))
                elif ind < self.current_player:
                    self.current_player = (self.current_player - 1) % len(self.queue)

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
            response.append(incoming_msg.encode(FORMAT))
            self.current_player += 1
            self.current_player %= len(self.queue)
            next_player = self.queue[self.current_player]
            broadcast = [*next_player.message_queue, f"TURN:{next_player.player_name}".encode(FORMAT)]

        elif request[0] == "START_GAME":
            self.started = True
            self.queue = self.players.copy()
            self.rank = len(self.players)
            response.append(f"{request[1]}: YOU HAVE STARTED THE GAME".encode(FORMAT))
            start_coords = spread_across_the_map(self.map_to_send, len(self.queue))
            for i, (y, x) in enumerate(start_coords):
                broadcast.append(f"ADD_UNIT:{self.queue[i].player_name}:{(x, y)}:Settler:1".encode(FORMAT))
            broadcast.append(f"TURN:{self.queue[0].player_name}".encode(FORMAT))

        elif request[0] == "EXIT_LOBBY":
            # TODO rethink Client.only_send() being used here
            # response.append(f"ALL_EXIT_LOBBY".encode(FORMAT))
            broadcast = [f"FINISH:::".encode(FORMAT)]

        elif request[0] == "QUIT_GAME":
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            self.players.remove(wanted)
            idx = self.players.index(wanted)
            self.connections[idx].close()
            self.connections.pop(idx)
            self.threads[idx].join()
            self.threads.pop(idx)

        elif request[0] == "END_GAME":
            # ranking = self.compute_rank(self.players)
            for player in self.players:
                player.rank = player.rank - len(self.queue) + 1 if player.rank else 1
            broadcast.append("GAME_ENDED".encode(FORMAT))
            broadcast.extend(str(f"RANK:{player.player_name}:{player.rank}").encode(FORMAT) for player in self.players)
            broadcast.append(incoming_msg.encode(FORMAT))
            self.finish = True

        elif request[0] == "ADD_UNIT" or request[0] == "MOVE_UNIT" or request[0] == "HEALTH":
            broadcast = [incoming_msg.encode(FORMAT)]

        elif request[0] == "ADD_CITY":
            wanted = next((player for player in self.players if player.player_name == request[1]), None)
            wanted.city_list.append(request[3])
            broadcast = [incoming_msg.encode(FORMAT)]

        elif request[0] == "MORE_AREA":
            broadcast = [incoming_msg.encode(FORMAT)]

        elif request[0] == "GIVE_CITY":
            broadcast = [incoming_msg.encode(FORMAT)]

            #####################################################################

        elif request[0].startswith("DIPLOMACY"):
            print("W diplo")
            # response.append(incoming_msg.encode(FORMAT))
            wanted = next((player for player in self.players if player.player_name == request[3]), None)
            if wanted is not None:
                wanted.message_queue.append(incoming_msg.encode(FORMAT))
            print("Po diplo")

        elif request[0] == "SEND_RESP":
            print("W przetwarzaniu odpowiedzi")
            sender = str(request[1])
            string_list = str(request[2])
            normal_list = eval(string_list)
            print(f"Lista po ewaluacji: {normal_list}")
            self.process_responses(normal_list)

        elif request[0] == "LIST_PLAYERS":
            response_list = []
            for player in self.players:
                response_list.extend([player.player_name])
            response_list_to_str = str(response_list)
            response.append(response_list_to_str.encode(FORMAT))

        elif request[0] == "LIST_MSGS":
            print("W list_msgs")
            player_nick = str(request[1])
            wanted = next((player for player in self.players if player.player_name == player_nick), None)
            msgs_list = wanted.message_queue
            msg_list_str = str(msgs_list)
            response.append(msg_list_str.encode(FORMAT))
            print("Po list_msgs")

        else:
            response.append(f"UNKNOWN OPTION".encode(FORMAT))
        return response, broadcast

    def connection_handler(self, conn, addr):
        """
        Oversees client-server communication. Is being run in its separate thread for each client.
        :param conn: socket object used to send and receive data to the client
        :param addr: client's address
        """
        connected = True
        while connected and not self.finish:
            try:
                msg_len = conn.recv(HEADER).decode(FORMAT)
            except socket.timeout:
                continue
            if msg_len:
                msg_len = int(msg_len)
                incoming_message = conn.recv(msg_len).decode(FORMAT)
                print_color(f"RECEIVED NEW MESSAGE: {incoming_message} from {addr}")
                if incoming_message == DISCONNECT_MESSAGE:
                    connected = False

                response, broadcast = self.parse_request(incoming_message, conn)
                if len(response) != 0:
                    response_length = self.header_generator(response[0])
                    conn.send(response_length)
                    conn.send(response[0])
                while broadcast:
                    mes = broadcast.pop(0)
                    for c in self.connections:
                        length = self.header_generator(mes)
                        c.send(length)
                        c.send(mes)

    def start_connection(self, server_socket):
        """
        Accepts a new client connection and creates a thread for handling it.
        """
        try:
            server_socket.listen()
            print_color(f"IM HERE: {HOST} {PORT}")
            while not self.started and not self.finish:
                try:
                    conn, addr = server_socket.accept()
                except socket.timeout:
                    continue
                self.connections[conn] = None
                conn.settimeout(1)
                print_color(f"NEW CONNECTION FROM {addr} ")
                new_thread = threading.Thread(target=self.connection_handler, args=(conn, addr))
                self.threads.append(new_thread)
                new_thread.start()
                print_color(f"N_O ACTIVE CONNECTIONS: {threading.activeCount() - 2}")
            for thread in self.threads:
                thread.join()

        except KeyboardInterrupt:
            for thread in self.threads:
                thread.join()
            print_color("SERVER PROCESS TERMINATED")


# for testing
if __name__ == "__main__":
    server = Server([1, 2])
