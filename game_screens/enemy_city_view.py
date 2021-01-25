import arcade
from arcade.gui import UIManager

from buy_goods_window import BuyGoodsWindow
from game_screens.city import City
from game_screens.popups import EnemyCityInfo


class EnemyCityView(arcade.View):
    def __init__(self, top_bar, app, client, me):
        super().__init__()
        self.city = None
        self.app = app
        self.top_bar = top_bar
        self.client = client
        self.me = me
        self.backup = None
        self.clicked_once = False

        self.ui_manager = UIManager()
        self.buy_city_button = None
        self.buy_goods_button = None
        self.declare_war_button = None
        self.propose_peace_button = None
        self.offer_alliance_button = None
        self.end_alliance_button = None

        self.sidebar_top = self.top_bar.size_y + 0.05
        popup_height = 0.2
        self.city_info = EnemyCityInfo(0.3, popup_height, self.sidebar_top)

        left, right, _, _ = self.city_info.coords_lrtb
        self.center_x = (left + right) / 2
        self.sidebar_width = right - left
        self.sidebar_top += popup_height + 0.025

        self.relative_button_height = 0.075
        self.button_height = int(self.relative_button_height * self.window.height)
        self.sidebar_top += self.relative_button_height / 2

    def set_city(self, city: City):
        self.city = city

    def on_show(self):
        arcade.start_render()

        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.city_info.display(self.city)
        self.top_bar.adjust()

        if True:
            self.buy_city_button = BuyCityButton(self, self.center_x, (1 - self.sidebar_top) * self.window.height,
                                                 self.sidebar_width, self.button_height)
            self.sidebar_top += self.relative_button_height + 0.025
            self.ui_manager.add_ui_element(self.buy_city_button)

        if True:
            self.buy_goods_button = BuyGoodsButton(self, self.center_x, (1 - self.sidebar_top) * self.window.height,
                                                   self.sidebar_width, self.button_height)
            self.sidebar_top += self.relative_button_height + 0.025
            self.ui_manager.add_ui_element(self.buy_goods_button)

        if True:
            self.declare_war_button = DeclareWarButton(self, self.center_x, (1 - self.sidebar_top) * self.window.height,
                                                       self.sidebar_width, self.button_height)
            self.sidebar_top += self.relative_button_height + 0.025
            self.ui_manager.add_ui_element(self.declare_war_button)

        if True:
            self.propose_peace_button = ProposePeaceButton(self, self.center_x,
                                                           (1 - self.sidebar_top) * self.window.height,
                                                           self.sidebar_width, self.button_height)
            self.sidebar_top += self.relative_button_height + 0.025
            self.ui_manager.add_ui_element(self.propose_peace_button)

        if True:
            self.offer_alliance_button = OfferAllianceButton(self, self.center_x,
                                                             (1 - self.sidebar_top) * self.window.height,
                                                             self.sidebar_width, self.button_height)
            self.sidebar_top += self.relative_button_height + 0.025
            self.ui_manager.add_ui_element(self.offer_alliance_button)

        if True:
            self.end_alliance_button = EndAllianceButton(self, self.center_x,
                                                         (1 - self.sidebar_top) * self.window.height,
                                                         self.sidebar_width, self.button_height)
            self.sidebar_top += self.relative_button_height + 0.025
            self.ui_manager.add_ui_element(self.end_alliance_button)

    def on_draw(self):
        img = arcade.load_texture(f"{self.city.path_to_visualization}")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)
        self.city_info.draw_background()
        self.top_bar.draw_background()
        self.clicked_once = True

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.city_info.hide()
        self.ui_manager.purge_ui_elements()
        self.clicked_once = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.back_to_game()
        else:
            pass


class BuyCityButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, y_position, width, height):
        super().__init__('Buy this city', center_x=center_x, center_y=y_position, width=width, height=height)
        self.parent = parent

    def on_click(self):
        # TODO Diplomacy procedure - 'buying city'
        if self.parent.clicked_once:
            print("Buying city procedure")
            self.parent.top_bar.update_treasury()
            self.parent.window.back_to_game()
        else:
            self.parent.clicked_once = True


class BuyGoodsButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, y_position, width, height):
        super().__init__('Buy goods', center_x=center_x, center_y=y_position, width=width, height=height)
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        if self.parent.clicked_once:
            win = BuyGoodsWindow(self, self.parent)
            win.show()
            self.app.exec_()
            self.parent.top_bar.update_treasury()
            print("exited buy goods.")
        else:
            self.parent.clicked_once = True

    def kill_app(self):
        self.app.exit()


class ProposePeaceButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, y_position, width, height):
        super().__init__('Propose peace', center_x=center_x, center_y=y_position, width=width, height=height)
        self.parent = parent

    def on_click(self):
        if self.parent.clicked_once:
            # TODO Diplomacy procedure - 'proposing peace'
            self.parent.client.send_truce_request(self.parent.city.owner.nick)

            print("Proposing peace procedure")
            self.parent.window.back_to_game()
        else:
            self.parent.clicked_once = True


class DeclareWarButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, y_position, width, height):
        super().__init__('Declare war', center_x=center_x, center_y=y_position, width=width, height=height)
        self.parent = parent

    def on_click(self):
        if self.parent.clicked_once:
            self.parent.client.declare_war(self.parent.city.owner.nick)

            print("Declaring war procedure")
            self.parent.window.back_to_game()
        else:
            self.parent.clicked_once = True


class OfferAllianceButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, y_position, width, height):
        super().__init__('Offer alliance', center_x=center_x, center_y=y_position, width=width, height=height)
        self.parent = parent

    def on_click(self):
        if self.parent.clicked_once:
            self.parent.client.send_alliance_request(self.parent.city.owner.nick)

            print("Offering alliance procedure")
            self.parent.window.back_to_game()
        else:
            self.parent.clicked_once = True


class EndAllianceButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, y_position, width, height):
        super().__init__('End alliance', center_x=center_x, center_y=y_position, width=width, height=height)
        self.parent = parent

    def on_click(self):
        if self.parent.clicked_once:
            self.parent.client.end_alliance(self.parent.city.owner.nick)

            print("Ending alliance procedure")
            self.parent.window.back_to_game()
        else:
            self.parent.clicked_once = True
