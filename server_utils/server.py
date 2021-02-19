import socket
import threading
from random import randint

from map_generation.spread_players import spread_across_the_map
from server_utils.player import Player

FORMAT = 'utf-8'
HEADER = 200



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
        self.colours = ['BUBBLE_GUM', 'CHERRY', 'PURPLE', 'CORAL']
        self.civilizations = ["The Great Northern", "Kaediredameria", "Mixtec", "Kintsugi"]
        self.current_player = 0  # index in self.players that indicates who is active
        self.rank = 0  # for now
        self.started = False
        self.finish = False
        self.sock = None
        self.ip = None
        self.port = None
        self.create_socket()

    def create_socket(self):
        """
        Initializes the server's socket.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind(('', 0))
        host = socket.gethostname()
        self.ip = socket.gethostbyname(host)
        self.port = self.sock.getsockname()[1]

    def header_generator(self, str_response):
        """
        Generates a proper header for a message.
        :param str_response: a message for which the header will be generated
        :return: the header containing the message length
        """
        resp_len = str(len(str_response)).encode(FORMAT)
        resp_len += b' ' * (HEADER - len(resp_len))
        return resp_len

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
                next_player = self.queue[ind]
                broadcast.extend(next_player.message_queue)
                broadcast.append(f"TURN:{next_player.player_name}".encode(FORMAT))
                next_player.message_queue.clear()
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
                    next_player = self.queue[ind]
                    broadcast.extend(next_player.message_queue)
                    broadcast.append(f"TURN:{next_player.player_name}".encode(FORMAT))
                    next_player.message_queue.clear()
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
            next_player.message_queue.clear()

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

        elif request[0].startswith("DIPLOMACY"):
            wanted = next((player for player in self.players if player.player_name == request[3]), None)
            if wanted is not None:
                wanted.message_queue.append(incoming_msg.encode(FORMAT))

        elif request[0] == "LIST_PLAYERS":
            response_list = []
            for player in self.players:
                response_list.extend([player.player_name])
            response_list_to_str = str(response_list)
            response.append(response_list_to_str.encode(FORMAT))

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
                if incoming_message[0] == 'DISCONNECT':
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

    def start_connection(self):
        """
        Accepts a new client connection and creates a thread for handling it.
        """
        try:
            self.sock.listen()
            print_color(f"IM HERE: {self.ip} {self.port}")
            while not self.started and not self.finish:
                try:
                    conn, addr = self.sock.accept()
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
