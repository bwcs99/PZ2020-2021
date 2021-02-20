class Player:

    def __init__(self, player_name, colour):
        self.player_name = player_name
        self.civilisation_type = ''
        self.active = True
        self.is_playername_set = True
        self.is_civilisation_set = False
        self.player_colour = colour
        self.treasury = 2000
        self.rank = None
        self.scores = 0
        self.city_list = []
        self.message_queue = []
        self.allies = []
        self.enemies = []

    def set_civilisation_type(self, civ_type):
        self.civilisation_type = civ_type
        self.is_civilisation_set = True
