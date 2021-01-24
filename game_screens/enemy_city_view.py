import arcade
from arcade.gui import UIManager

from buy_goods_window import BuyGoodsWindow
from game_screens.city import City


class EnemyCityView(arcade.View):
    def __init__(self, top_bar, app):
        super().__init__()
        self.city = None
        self.app = app
        self.top_bar = top_bar
        self.backup = None
        self.ui_manager = UIManager()
        self.buy_city_button = None
        self.buy_goods_button = None
        self.declare_war_button = None
        self.propose_peace_button = None

    def set_city(self, city: City):
        self.city = city

    def on_show(self):
        arcade.start_render()

        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.top_bar.adjust()

        # TODO Diplomacy - add handling which buttons should be displayed in particular diplomacy situation.

        self.buy_city_button = BuyCityButton(self, center_x=self.window.width, center_y=self.window.height)
        self.ui_manager.add_ui_element(self.buy_city_button)

        self.buy_goods_button = BuyGoodsButton(self, center_x=self.window.width,
                                               center_y=self.window.height)
        self.ui_manager.add_ui_element(self.buy_goods_button)
        self.declare_war_button = DeclareWarButton(self, center_x=self.window.width, center_y=self.window.height)
        self.ui_manager.add_ui_element(self.declare_war_button)
        self.propose_peace_button = ProposePeaceButton(self, center_x=self.window.width,
                                                       center_y=self.window.height)
        self.ui_manager.add_ui_element(self.propose_peace_button)

    def on_draw(self):
        img = arcade.load_texture(f"{self.city.path_to_visualization}")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)
        self.top_bar.draw_background()

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.ui_manager.purge_ui_elements()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.back_to_game()
        else:
            pass


class BuyCityButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Buy this city', center_x=center_x // 2 - 300, center_y=center_y // 4, width=250, )
        self.parent = parent

    def on_click(self):
        # TODO Diplomacy procedure - 'buying city'

        print("Buying city procedure")
        self.parent.top_bar.update_treasury()
        self.parent.window.back_to_game()


class BuyGoodsButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Buy goods', center_x=center_x // 2 - 300, center_y=center_y // 4 - 100, width=250, )
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        win = BuyGoodsWindow(self, self.parent)
        win.show()
        self.app.exec_()
        self.parent.top_bar.update_treasury()
        print("exited buy goods.")

    def kill_app(self):
        self.app.exit()


class ProposePeaceButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Propose peace', center_x=center_x // 2 + 300, center_y=center_y // 4, width=250, )
        self.parent = parent

    def on_click(self):
        # TODO Diplomacy procedure - 'proposing peace'

        print("Proposing peace procedure")
        self.parent.window.back_to_game()


class DeclareWarButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Declare war', center_x=center_x // 2 + 300, center_y=center_y // 4 - 100, width=250, )
        self.parent = parent

    def on_click(self):
        # TODO Diplomacy procedure - 'declaring war'

        print("Declaring war procedure")
        self.parent.window.back_to_game()
