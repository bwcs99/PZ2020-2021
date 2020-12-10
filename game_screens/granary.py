class Granary:
    """
    Class representing concept of resources gathered in one place.
    Now when I think about it... It all should be dictionary.
    Maybe we will survive without it.
    """

    def __init__(self, gold: int = 0, wood: int = 0, stone: int = 0, food: int = 0):
        self.gold = gold
        self.wood = wood
        self.stone = stone
        self.food = food

    def __str__(self):
        return f" In granary there is " \
               f"gold = {self.gold}, wood = {self.wood}, stone = {self.stone}, food = {self.food}, Master."

    def empty_granary(self):
        self.gold = 0
        self.wood = 0
        self.stone = 0
        self.food = 0

    def insert_from(self, granary):
        """
        Method for transporting, stealing, harvesting from one granary directly to another. After that "from" granary will be
        empty.
        :param granary: granary from which materials will be taken.
        """
        self.gold += granary.gold
        self.wood += granary.wood
        self.stone += granary.stone
        self.food += granary.food
        granary.empty_granary()

    def is_enough(self, costs: dict):
        if self.gold >= costs["gold"] and self.wood >= costs["wood"] and self.stone >= costs["stone"] and self.food >= \
                costs["food"]:
            return True
        else:
            return False

    def pay_for(self, costs: dict):
        if self.is_enough(costs):
            self.gold -= costs["gold"]
            self.wood -= costs["wood"]
            self.stone -= costs["stone"]
            self.food -= costs["food"]
        else:
            raise ArithmeticError

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
