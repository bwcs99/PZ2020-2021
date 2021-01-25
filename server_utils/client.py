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
        try:
            self.sock.connect(ADDR)
        except ConnectionRefusedError as e:
            return f'Game is not hosted yet!'

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

    def add_unit(self, x, y, unit_type, count):
        """
        Adds a unit of the specified type on tile (x,y). It's owner is the player sending the message since only
        they can create a unit for themself.
        """
        msg = f"ADD_UNIT:{self.nick}:({x},{y}):{unit_type}:{count}"
        print(msg, "-test")
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

    ''' Funkcja do wysyłania propozycji sojuszu'''
    def send_alliance_request(self, sender, receiver, sender_allies):
        """ param1: (str) nadawca, param2: (str) odbiorca, param3: lista sojuszników (list of strings/nicks)"""
        if receiver in sender_allies:
            return f'{receiver} is already your allie'
        else:
            msg = f'ALLIANCE:{sender}:{receiver}:{False}'
            self.only_send(msg)

    ''' Funkcja do pobierania listy wiadomości z serwera'''
    def get_messages_from_server(self, sender):
        """ param1: nadawca (str)
        return - lista wiadomości z serwera (lista stringów) """
        msg = f'LIST_MSGS:{sender}'
        resp = self.send_msg(msg)
        msg_queue = eval(resp)
        return msg_queue

    ''' Funkcja do zrywania sojuszy z innymi graczami'''
    def end_alliance(self, sender, receiver, sender_allies):
        """param1: nadawca (str), param2: odbiorca (str), param3: lista sojuszników (list of strings/nicks)"""
        if receiver not in sender_allies:
            return f'{receiver} is not your allie, so you cant end alliance with him'
        else:
            msg = f'END_ALLIANCE:{sender}:{receiver}:{False}'
            self.only_send(msg)

    ''' Funkcja służaca do wypowiadania wojny'''
    def declare_war(self, sender, receiver, sender_enemies):
        """ param1: nadawca (str), param2: odbiorca (str), param3: lista wrogów (list of stringd/nicks)"""
        if receiver in sender_enemies:
            return f'{receiver} is already your enemy'
        else:
            msg = f'DECLARE_WAR:{sender}:{receiver}:{False}'
            self.only_send(msg)

    '''' Podczas wojny możemy się poddać'''
    def give_up(self, sender, receiver, sender_enemies):
        """ param1: nadawca (str), param2: odbiorca (str), param3: lista wrogów (list of stringd/nicks)"""
        if receiver in sender_enemies:
            return f'{receiver} is already your enemy'
        else:
            msg = f'GIVE_UP:{sender}:{receiver}:{False}'
            self.only_send(msg)

    ''' Lub zaproponować rozejm'''
    def send_truce_request(self, sender, receiver, sender_enemies):
        """ param1: nadawca (str), param2: odbiorca (str), param3: lista wrogów (list of stringd/nicks)"""
        if receiver not in sender_enemies:
            return f'{receiver} is not your enemy, so you cant send truce request to him'
        else:
            msg = f'TRUCE:{sender}:{receiver}:{False}'
            self.only_send(msg)

    ''' Wysyłanie propozycji kupna'''
    def send_buy_request(self, sender, receiver, price, resource, my_granary,
                         seller_granary, is_city=False, city_cords=(), quantity=1):
        """ param1 : nick nadawcy (str), param2 : nick odbiorcy (str), param3: proponowana cena (int),
        param4: nazwa surowca (str),
        param5: mój skarbiec (granary), param6: skarbiec sprzedawcy (granary),
        param6: czy sprzedajemy miasto (bool), param7: wsp. miasta (tuple: (x: int, y: int)),
        param8: ilość surowca/miasta (dla miast domyślna ilośc to 1) (int)
         return - w razie jakichś problemów zwraca odpowiedni komunikat błędu"""
        if my_granary.gold < price:
            return f'You cant afford it'
        if resource == 'food':
            if seller_granary.food < quantity:
                return f'{receiver} has not enough resource of this kind'
        elif resource == "stone":
            if seller_granary.stone < quantity:
                return f'{receiver} has not enough resource of this kind'
        elif resource == "wood":
            if seller_granary.wood < quantity:
                return f'{receiver} has not enough resource of this kind'
        else:
            resource_tuple = ()
            if is_city:
                resource_tuple = (is_city, city_cords)
            else:
                resource_tuple = (is_city, resource)
            msg = f'BUY:{sender}:{receiver}:{str(resource_tuple)}:{price}:{quantity}:{False}'
            self.only_send(msg)

    '''Wysyłanie propozycji sprzedaży'''
    def send_sell_request(self, sender, receiver, price, resource, my_granary, buyer_granary, quantity=1):
        """ param1: nadawca (str), param2: odbiorca (str), param3: cena (int),
        param4: surowiec (str), param5: mój skarbiec (granary), param6: skarbiec
        kupca (granary), param7: ilość surowca (int)
         return - w razie jakichś problemów zwraca odpowiedni komunikat błędu"""
        if buyer_granary.gold < price:
            return f'{receiver} cant afford it'
        if resource == 'food':
            if my_granary.food < quantity:
                return f'You have not enough resource of this kind'
        elif resource == 'stone':
            if my_granary.stone < quantity:
                return f'You have not enough resource of this kind'
        elif resource == 'wood':
            if my_granary.wood < quantity:
                return f'You have not enough resource of this kind'
        else:
            msg = f'SELL:{sender}:{receiver}:{resource}:{price}:{quantity}:{False}'
            self.only_send(msg)

    ''' Wysyłamy nasze odpowiedzi na serwer i serwer wysyła je do odpowiednich graczy'''
    def send_response_to_players(self, sender, response_list):
        """param1: nadawca (str), param2: lista odpowiedzi (list of strings) """
        msg = f'SEND_RESP:{sender}:{str(response_list)}'
        self.only_send(msg)

    ''' Rozpatrujemy propozycje innych graczy '''
    def create_answer(self, msg, decision=True):
        """param1: odpowiedź (str), param2: roztrzygnięcie (bool: True lub False) (pozytywne/negatywne)
        return - odpowiedź - pozytywna/negatywna """
        splited_msg = msg.split(":")
        splited_msg[0] += "_ANSWER"
        if decision:
            splited_msg[-1] = str(True)
        else:
            splited_msg[-1] = str(False)
        ans = ':'.join(splited_msg)
        return ans

    def display_message_to_others(self, messages):
        """ Wyświetla wiadomości dostępne powszechnie. param1: lista wiadomości (lista stringów),
        return - odpowiednio spreparowane zdania do wyświetlenia. Z tą funkcją jest podobnie jak z poniższą """
        information_list = []
        for message in messages:
            fields_values = message.split(":")
            if "EAL_INFO" in message:
                information_list.extend([f'Alliance between {fields_values[1]} and {fields_values[2]} ended'])
            elif "DCL_WAR_INFO" in message:
                information_list.extend([f'{fields_values[1]} has declared war to {fields_values[2]}'])
            elif "ALC_INFO" in message:
                information_list.extend([f'{fields_values[1]} and {fields_values[2]} are allies'])
            elif "GUP_INFO" in message:
                information_list.extend([f'{fields_values[1]} gave up. War between {fields_values[1]}'
                                         f'and {fields_values[2]} ended'])
            elif "TRC_INFO" in message:
                information_list.extend([f'{fields_values[1]} sent truce request to {fields_values[2]}. War between'
                                         f'them is ended'])
            elif "B_INFO" in message:
                cords = eval(fields_values[-1])
                # zamiast współrzędnych przydałaby się nazwa
                information_list.extend([f'{fields_values[1]} has bought {cords} city from {fields_values[2]}'])
        return information_list


    ''' Dla Patryka - zwraca napis będący odpowiednim komunikatem. Dzięki temu będziemy musieli tylko podpiąć jakieś
    okno do wyświetlania wiadomości. To wcale nie musi być w klasie klienckiej (a nawet chyba nie powinno) '''
    def display_message_queue(self, messages):
        """param1: lista wiadomości danego użytkownika (z serwera) (list of strings)
        return - lista stringów (odpowiednio spreparowanych zdań)"""
        information_list = []
        for message in messages:
            value_fields = message.split(":")
            if "END_ALLIANCE" in message:
                if "ANSWER" in message:
                    information_list.extend([f'Alliance between you and {value_fields[2]} ended'])
                else:
                    information_list.extend([f'Your ally {value_fields[1]} wants to end alliance with you'])
            elif "ALLIANCE" in message:
                if "ANSWER" in message:
                    if bool(value_fields[-1]):
                        information_list.extend([f'You and {value_fields[2]} are allies'])
                    else:
                        information_list.extend([f'{value_fields[2]} doesnt want to be ally with you'])
                else:
                    information_list.extend([f'{value_fields[1]} wants alliance with you'])
            elif "DECLARE_WAR" in message:
                if "ANSWER" in message:
                    information_list.extend([f'{value_fields[2]} knows. Now you can attack each other'])
                else:
                    information_list.extend([f'{value_fields[1]} has declared war to you'])
            elif "GIVE_UP" in message:
                if "ANSWER" in message:
                    information_list.extend([f'{value_fields[2]} knows. War is ended. You lost it'])
                else:
                    information_list.extend([f'{value_fields[1]} wants to give up'])
            elif "TRUCE" in message:
                if "ANSWER" in message:
                    if bool(value_fields[-1]):
                        information_list.extend([f'{value_fields[2]} thinks its good idea! War is ended'])
                    else:
                        information_list.extend([f'{value_fields[2]} doesnt want peace'])
                else:
                    information_list.extend([f'{value_fields[1]} wants to end this war'])
            elif "BUY" in message:
                res_tup = eval(value_fields[3])
                is_city = bool(res_tup[0])
                res_name = res_tup[1]
                if "ANSWER" in message:
                    if bool(value_fields[-1]):
                        information_list.extend([f'{value_fields[2]} was interested. The transaction ended successfully'])
                    else:
                        information_list.extend([f'{value_fields[2]} was not interested. The transaction failed'])
                else:
                    if is_city:
                        information_list.extend(
                            [f'{value_fields[1]} wants to buy {res_name} city from you. Qunatity: {value_fields[-2]}. '
                            f'Price: {value_fields[-3]}'])
                    else:
                        information_list.extend(
                            [f'{value_fields[1]} wants to buy {res_name} from you. Qunatity: {value_fields[-2]}.'
                            f'Price: {value_fields[-3]}'])

            elif "SELL" in message:
                res_tup = eval(value_fields[1])
                is_city = bool(res_tup[0])
                res_name = res_tup[1]
                if "ANSWER" in message:
                    if bool(value_fields[-1]):
                        information_list.extend([f'{value_fields[3]} was interested. The transaction ended successfully'])
                    else:
                        information_list.extend([f'{value_fields[3]} was not interested. The transaction failed'])
                else:
                    if is_city:
                        information_list.extend(
                            [f'{value_fields[1]} wants to sell you {res_name} city. Qunatity: {value_fields[-2]}.'
                            f'Price: {value_fields[-3]}'])
                    else:
                        information_list.extend(
                            [f'{value_fields[1]} wants to sell you {res_name}. Qunatity: {value_fields[-2]}.'
                            f'Price: {value_fields[-3]}'])
        return information_list







