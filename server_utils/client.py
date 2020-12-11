import ast
import socket

# Dane potrzebne do połączenia się z serwerem
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 200
DISCONNECT_MESSAGE = "DISCONNECT"


class Client:
    """
    Client class for application.
    It handles connection to server, sending and getting messages.
    It sends requests as -> <REQUEST>:::.
    Which is afterwards smartly handled by server.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.available_civilizations = None
        self.current_players_on_server = None
        self.nick = None
        self.players = []
        self.started = False


    # This method listens for messages from server.
    def rec_msg(self):
        msg_len = self.sock.recv(HEADER).decode(FORMAT)
        incoming_msg = ""
        if msg_len:
            incoming_msg = self.sock.recv(int(msg_len)).decode(FORMAT)
        return incoming_msg

    # This method sends requests on server and expects response.
    def send_msg(self, msg):
        message = msg.encode(FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(message)
        # print("THE MESSAGE HAS BEEN SENT")
        # print(sock.recv(2048).decode(FORMAT))
        response = self.rec_msg()
        if response:
            # print("TU")
            # print(response)
            pass
        return response

    # This method sends request and DOES NOT expect response.
    def only_send(self, msg):
        message = msg.encode(FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(message)

    # Standard connection method
    def connect(self):
        self.sock.connect(ADDR)

    # Standard disconnection method
    def disconnect(self):
        self.only_send(f"DISCONNECT:{self.nick}")
        self.sock.shutdown(socket.SHUT_RDWR)

    def die(self):
        msg = f"DEFEAT:{self.nick}"
        self.only_send(msg)
        return self.unexpected_messages(msg)

    def kill(self, player):
        msg = f"DEFEAT:{player}"
        self.only_send(msg)
        return self.unexpected_messages(msg)

    # Method allowing to send basic info to server
    def introduce_yourself(self, chosen_nick, chosen_civ):
        # TODO maybe only_send?
        self.nick = chosen_nick
        self.send_msg("ADD_NEW_PLAYER:" + chosen_nick + "::")
        self.send_msg("CHOOSE_CIVILISATION:" + chosen_nick + ":" + chosen_civ + ":")
        self.rec_msg()

    # Method sends request for available civilizations and gets response
    def get_available_civilizations_from_server(self):
        self.available_civilizations = self.send_msg("LIST_CIVILIZATIONS:::")
        return self.available_civilizations

    # Standard getter
    def get_available_civilizations(self):
        self.get_available_civilizations_from_server()
        return self.available_civilizations

    # Method sends request for current players and gets response
    def get_current_players_from_server(self):
        self.current_players_on_server = self.send_msg("LIST_PLAYERS:::")
        return self.current_players_on_server

    # Standard getter
    def get_current_players(self):
        self.get_current_players_from_server()
        return self.current_players_on_server

    # Standard setter
    def set_nickname(self, nick):
        self.nick = nick

    # Method gets map from server
    def get_map_from_server(self):
        map_from_server = self.send_msg("SHOW_MAP:::")
        return map_from_server

    # Method used only by server to inform all connected clients to begin exit lobby procedure
    def exit_lobby(self):
        self.only_send("EXIT_LOBBY:::")

    # Method used only by server to inform all connected clients to begin start game procedure
    def start_game(self):
        self.send_msg("START_GAME:::")

    # Widely used method by every client to inform about ending your turn
    def end_turn(self):
        msg = f"END_TURN:{self.nick}::"
        try:
            self.only_send(msg)
            return self.unexpected_messages(msg)
        except OSError:
            return self.unexpected_messages("END_GAME")

    # This method is called when new player connects to server.
    # Difference between this method and get_current_players_from_server is
    # that this one only receives from server freshly connected player.
    def get_new_player(self):
        new_player = self.rec_msg()
        return new_player.split(":")

    def get_opponents_move(self):
        """
        Used while the player is waiting for their turn. Waits for a server message describing an action (turn end,
        unit moved, etc.) and parses it to a form that game_view is able to understand - a tuple of (ACTION, args...),
        for instance ("TURN", name of the player whose turn begins) or ("MOVE", x0, y0, x1, y1) when a unit is moved
        from (x0, y0) to (x1, y1).
        """
        try:
            mes = self.rec_msg()
            if not mes:
                return ["DISCONNECTED"]
            return mes.split(':')
        except OSError:
            return ["DISCONNECTED"]

    """ Funkcja służąca do kończenia gry przez hosta """
    def end_game_by_host(self):
        self.only_send("END_GAME")
        return self.unexpected_messages("END_GAME")

    """ Funkcja służąca do kończenia gry przez danego gracza """
    def quit_game(self, player_nick):
        self.only_send("QUIT_GAME:"+player_nick+"::")

    """ Funkcja zwiększająca stan skarbca danego gracza """
    def more_money(self, number, player_nick):
        self.only_send("MORE_MONEY:"+player_nick+":"+str(number)+":")

    """ Funkcja zmniejszająca stan skarbca danego gracza """
    def less_money(self, number, player_nick):
        self.only_send("LESS_MONEY:"+player_nick+":"+str(number)+":")

    """ Funkcja zwracjąca aktualny stan skarbca danego gracza """
    def get_treasury_state(self, player_nick):
        state = self.send_msg("GET_TREASURY:"+player_nick+"::")
        return int(state)

    """ Służy do doawania punktów konkretnemu graczowi (tu trzeba opracować polityke przyznawania punktów)"""
    def add_scores(self, new_scores, player_nick):
        self.only_send("ADD_SCORES:"+player_nick+":"+str(new_scores)+":")

    """ Wysyłanie zmienionej mapy na serwer (move_unit i put_unit w jednym przy założeniu, że zmiany na mapach
    odbywają się po stronie klienta) """
    # być może przyda się w momencie gdy ktoś będzie out of sync, ale ja na razie wolałem to zrobić tak jak niżej /P
    def send_changed(self, changed_map):
        map_to_str = str(changed_map)
        self.only_send("CHANGE_MAP:"+":"+map_to_str+":")

    def move_unit(self, x0, y0, x1, y1, cost):
        """ Moves the unit located on the tile (x0, y0) to the tile (x1, y1) at a specified cost."""
        msg = f"MOVE_UNIT:({x0},{y0}):({x1},{y1}):{cost}"
        try:
            self.only_send(msg)
            return self.unexpected_messages(msg)
        except OSError:
            return self.unexpected_messages("END_GAME")

    def add_unit(self, x, y, unit_type):
        """
        Adds a unit of the specified type on tile (x,y). It's owner is the player sending the message since only
        they can create a unit for themself.
        """
        msg = f"ADD_UNIT:{self.nick}:({x},{y}):{unit_type}"
        try:
            self.only_send(msg)
            return self.unexpected_messages(msg)
        except OSError:
            return self.unexpected_messages("END_GAME")

    def update_health(self, x, y, new_health):
        msg = f"HEALTH:{(x, y)}:{new_health}"
        try:
            self.only_send(msg)
            return self.unexpected_messages(msg)
        except OSError:
            return self.unexpected_messages("END_GAME")

    def get_city(self, city):
        msg = f"GIVE_CITY:{city.tile.coords}:{self.nick}"
        try:
            self.only_send(msg)
            return self.unexpected_messages(msg)
        except OSError:
            return self.unexpected_messages("END_GAME")

    """ Funkcja do wylistowania wszystkich miast """
    def get_cities_from_server(self):
        rep = self.send_msg("LIST_CITIES:::")
        return eval(rep)

    def add_city(self, x, y, city_name):
        """ Adds a city with the specified name on tile (x, y). It's owner is the player sending the message. """
        msg = f"ADD_CITY:{self.nick}:({x},{y}):{city_name}"
        try:
            self.only_send(msg)
            return self.unexpected_messages(msg)
        except OSError:
            return self.unexpected_messages("END_GAME")

    def unexpected_messages(self, msg):
        """
        A generator of messages that were received between sending a request to the server and getting a confirmation.
        :param msg: the message that was sent to the server, we're waiting to receive the same message as confirmation
        """
        new_msg = None
        while new_msg != msg:
            new_msg = self.rec_msg()
            yield new_msg.split(":")
