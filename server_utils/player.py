import sys

# Klasa definiująca gracza i podstawowe informacje z nim związane


class Player:

    def __init__(self, player_name, colour):
        # imię
        self.player_name = player_name
        # typ cywilizacji
        self.civilisation_type = ''
        # czy aktywny
        self.active = True
        # czy ma ustawiony nick
        self.is_playername_set = True
        # czy wybrał cywilizacje (wybór cywilizacji jest opcjonalny)
        self.is_civilisation_set = False
        # kolor gracz
        self.player_colour = colour
        ''' Nowa rzecz - skarbiec gracza '''
        self.treasury = 2000
        ''' Ranking  - potrzebny przy określanu miejsc na koniec '''
        self.rank = None
        ''' Liczba punktów - na jej podstawie tworzony jest ranking '''
        self.scores = 0
        ''' Lista miast należących do gracza'''
        self.city_list = []
        ''' Kolejka z wiadomościami '''
        self.message_queue = []
        ''' Lista sojuszników gracza - na razie można mieć max 2 sojuszników'''
        self.allies = []
        ''' Lista graczy, z którymi jesteśmy w stanie wojny'''
        self.enemies = []

    def set_civilisation_type(self, civ_type):
        self.civilisation_type = civ_type
        self.is_civilisation_set = True


