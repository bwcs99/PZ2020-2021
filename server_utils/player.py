import sys

# Klada definiająca gracza i podstawowe informacje z nim związane
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
        self.message_queue = []
    def set_civilisation_type(self, civ_type):
        self.civilisation_type = civ_type
        self.is_civilisation_set = True
       


    