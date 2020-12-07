class Granary:
    def __init__(self, gold: int = 0, wood: int = 0, stone: int = 0, food: int = 0):
        self.gold = gold
        self.wood = wood
        self.stone = stone
        self.food = food

    def empty_granary(self):
        self.gold = 0
        self.wood = 0
        self.stone = 0
        self.food = 0

    def insert_from(self, granary):
        """
        Method for transporting, stealing, harvesting from one granary directly to another. After that granary will be
        empty.
        :param granary: granary from which materials will be taken.
        """
        self.gold += granary.gold
        self.wood += granary.wood
        self.stone += granary.stone
        self.food += granary.food
        granary.empty_granary()

    """Following methods are used to adding materials to granary."""

    def add_gold(self, number: int):
        self.gold += number

    def add_wood(self, number: int):
        self.wood += number

    def add_stone(self, number: int):
        self.stone += number

    def add_food(self, number: int):
        self.food += number

    """ Following methods are used for subtracting materials from granary.
    Main logic behind using them is ass follow:
    1. I am paying for something e.g. building unit: 
        if my_granary.try_to_sub_*(2137):
        T -> continue, number subtracted
        F -> print("You don't have enough"), nothing happens to granary
    """

    def try_to_sub_gold(self, number: int) -> bool:
        if self.gold < number:
            return False
        else:
            self.gold -= number
            return True

    def try_to_sub_wood(self, number: int) -> bool:
        if self.wood < number:
            return False
        else:
            self.wood -= number
            return True

    def try_to_sub_stone(self, number: int) -> bool:
        if self.stone < number:
            return False
        else:
            self.stone -= number
            return True

    def try_to_sub_food(self, number: int) -> bool:
        if self.food < number:
            return False
        else:
            self.food -= number
            return True
