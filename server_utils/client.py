import socket

# Dane potrzebne do połączenia się z serwerem
PORT = 65001
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "DISCONNECT"

"""	Gabi:
	- potrzebuję konstruktor, która tworzy clienta.
	- potrzebuję metodę connect(address), gdzie address to adres serwera, na ten moment może być 127.0.0.1, ale możemy stwarzać pozory, że ma się to łączyć z innymi urzadzeniami.
	ta metoda nawiązuję pierwsze połączenie i nic więcej.
	- potrzebuję get_available_civilizations_from_server(), metoda pobiera jeszcze niewykorzystane cywilizacje z serwera, niech zapisuje je w self.available_civilizations
	- potrzebuję get_available_civilizations(), publiczna metoda zwraca self.available_civilizations, potrzebne w connect_window.py
	- potrzebuję procedury dodania do serwera gracza poprzez wysłanie nicku i cywilizacji do serwera. Metoda introduce_yourself(nick, civ) (to w zasadzie scenariusz z ADD_NEW_PLAYER i CHOOSE_CIVILIZATION jednoczesnie).
	- potrzebuję get_current_players_from_server(), metoda zwraca wszystkich graczy, których trzyma serwer, w postaci [["Nickname1", "Civilization1", "Color1"], ["Nickname2", "Civilization2", "Color2"], ...],
	niech zapisuje je w self.current_players_on_server.
	- potrzebuję get_current_players(), publiczna metoda zwraca self.current_players_on_server, potrzebne w connect_window.py
	- potrzebuję aby klient nasłuchiwał na inormacje o tym, że został dodany nowy gracz.
	
"""


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.available_civilizations = None
        self.current_players_on_server = None

    # def prepare_initial_msg(nick):
    #	return f"ADD_NEW_PLAYER:{nick}"

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

    # Funkcja służąca do łączenia się z serwerem + obsługa błędów
    def connect_to_server(self):
        try:
            print("TYPE YOUR NICK BELOW: ")
            nick = str(input())
            self.send_msg(nick)
            while True:
                msg_to_send = str(input())
                self.send_msg(msg_to_send)
                if msg_to_send == DISCONNECT_MESSAGE:
                    break
        except KeyboardInterrupt:
            print("CLIENT PROCESS TERMINATED")

    def connect(self):
        self.sock.connect(ADDR)

    def disconnect(self):
        self.send_msg(DISCONNECT_MESSAGE)
        self.sock.close()

    def get_available_civilizations_from_server(self):
        pass

    def get_available_civilizations(self):
        return self.available_civilizations

    def get_current_players_from_server(self):
        pass

    def get_current_players(self):
        return self.current_players_on_server

# connect_to_server()
