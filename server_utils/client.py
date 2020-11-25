import ast
import socket

# Dane potrzebne do połączenia się z serwerem
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 200
DISCONNECT_MESSAGE = "DISCONNECT"

"""	Gabi:
	- potrzebuję konstruktor, która tworzy clienta. 
	- potrzebuję metodę connect(address), gdzie address to adres serwera, na ten moment może być 127.0.0.1, ale możemy stwarzać pozory, że ma się to łączyć z innymi urzadzeniami.	ta metoda nawiązuję pierwsze połączenie i nic więcej. ok
	- potrzebuję get_available_civilizations_from_server(), metoda pobiera jeszcze niewykorzystane cywilizacje z serwera, niech zapisuje je w self.available_civilizations
	- potrzebuję get_available_civilizations(), publiczna metoda zwraca self.available_civilizations, potrzebne w connect_window.py
	- potrzebuję procedury dodania do serwera gracza poprzez wysłanie nicku i cywilizacji do serwera. Metoda introduce_yourself(nick, civ) (to w zasadzie scenariusz z ADD_NEW_PLAYER i CHOOSE_CIVILIZATION jednoczesnie).
	- potrzebuję get_current_players_from_server(), metoda zwraca wszystkich graczy, których trzyma serwer, w postaci [["Nickname1", "Civilization1", "Color1"], ["Nickname2", "Civilization2", "Color2"], ...],
	niech zapisuje je w self.current_players_on_server.
	- potrzebuję get_current_players(), publiczna metoda zwraca self.current_players_on_server, potrzebne w connect_window.py
	- potrzebuję aby klient nasłuchiwał na inormacje o tym, że został dodany nowy gracz.
	- potrzebuję get_map_from_server(), metoda zwraca macierz mapy 
"""

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.available_civilizations = None
        self.current_players_on_server = None
        self.nick = None

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
        send_length += b' ' * (HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(message)
        # print("THE MESSAGE HAS BEEN SENT")
        # print(sock.recv(2048).decode(FORMAT))
        response = self.rec_msg()
        if response:
            # print("TU")
            print(response)
        return response

    def only_send(self, msg):
        message = msg.encode(FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(message)

    def connect(self):
        self.sock.connect(ADDR)

    def disconnect(self):
        self.send_msg(DISCONNECT_MESSAGE)
        self.sock.close()

    def introduce_yourself(self, chosen_nick, chosen_civ):
        self.nick = chosen_nick
        self.send_msg("ADD_NEW_PLAYER:" + chosen_nick + "::")
        self.send_msg("CHOOSE_CIVILISATION:" + chosen_nick + ":" + chosen_civ + ":")
        self.rec_msg()

    # jak w opisie
    def get_available_civilizations_from_server(self):
        self.available_civilizations = self.send_msg("LIST_CIVILIZATIONS:::")
        return self.available_civilizations

    # jak w opisie
    def get_available_civilizations(self):
        self.get_available_civilizations_from_server()
        return self.available_civilizations

    # jak w opisie
    def get_current_players_from_server(self):
        self.current_players_on_server = self.send_msg("LIST_PLAYERS:::")
        return self.current_players_on_server

    # jak w opisie
    def get_current_players(self):
        self.get_current_players_from_server()
        return self.current_players_on_server

    # jak w opisie
    def set_nickname(self, nick):
        self.nick = nick

    # jak w opisie
    def get_map_from_server(self):
        map = self.send_msg("SHOW_MAP:::")
        return map

    def start_game(self):
        self.send_msg("START_GAME:::")

    def exit_lobby(self):
        self.only_send("EXIT_LOBBY:::")

    def end_turn(self):
        self.send_msg("END_TURN:::")

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
        mes = self.rec_msg()
        turn, name = ast.literal_eval(mes)
        return turn, name
