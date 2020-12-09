import threading

import arcade
import arcade.gui

from city_view import CityView
from .popups import TopBar, UnitPopup, CityCreationPopup, FONT_COLOR
from .game_logic import GameLogic
from .tiles import Tile

TOP_BAR_SIZE = 0.0625  # expressed as the percentage of the current screen height
UNIT_POPUP_SIZE = 3 * TOP_BAR_SIZE

SCROLL_STEP = 0.125  # new_height = old_height +- 2 * scroll_step * original_height, same with width
MAX_ZOOM = int(1 / (2 * SCROLL_STEP))

# TILE_ROWS = 25
# TILE_COLS = 40
MARGIN = 1  # space between two tiles (vertically & horizontally) in pixels (while fully zoomed out)


class GameView(arcade.View):
    """
    The view of the map of the game.
    """

    def __init__(self, width: int, height: int, tiles: list, client):
        """
        :param width: Max screen width.
        :param height: Max screen height.
        :param tiles: A 2D list of integer values representing tile types.
        :param client: A client object for server communication.
        """
        super().__init__()
        arcade.gui.elements.UIStyle.set_class_attrs(
            arcade.gui.elements.UIStyle.default_style(),
            "label",
            font_name="resources/fonts/november",
            font_color=FONT_COLOR,
            font_size=64
        )
        arcade.gui.elements.UIStyle.set_class_attrs(
            arcade.gui.elements.UIStyle.default_style(),
            "inputbox",
            font_name="resources/fonts/november"
        )

        self.client = client
        self.my_turn = False
        self.cur_enemy = ""

        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.SCROLL_STEP_X = SCROLL_STEP * width
        self.SCROLL_STEP_Y = SCROLL_STEP * height
        self.TILE_ROWS = len(tiles)
        self.TILE_COLS = len(tiles[0])
        self.zoom = 0

        self.top_bar = TopBar(TOP_BAR_SIZE)
        self.unit_popup = UnitPopup(4 * TOP_BAR_SIZE, 3 * TOP_BAR_SIZE)
        self.update_popup = False  # used to only update pop-up once per opponent's move, otherwise game is laggy
        self.city_popup = CityCreationPopup(4 * TOP_BAR_SIZE, 5 * TOP_BAR_SIZE)
        self.tiles = tiles

        self.tile_sprites = arcade.SpriteList()
        # needs to be smarter tbh but depends on the size of a real map
        self.tile_size = int((height - self.top_bar.height) / self.TILE_ROWS) - MARGIN
        # in order to center the tiles vertically and horizontally
        self.centering_x = (width - self.TILE_COLS * (self.tile_size + MARGIN)) / 2
        self.centering_y = ((height - self.top_bar.height) - self.TILE_ROWS * (self.tile_size + MARGIN)) / 2

        for row in range(self.TILE_ROWS):
            for col in range(self.TILE_COLS):
                tile = Tile(col, row, self.tile_size, tiles[row][col])
                tile.center_x = col * (self.tile_size + MARGIN) + (self.tile_size / 2) + MARGIN + self.centering_x
                tile.center_y = row * (self.tile_size + MARGIN) + (self.tile_size / 2) + MARGIN + self.centering_y
                self.tile_sprites.append(tile)

        self.game_logic = GameLogic(self.tile_sprites, self.TILE_ROWS, self.TILE_COLS, self.client.players, self.client.nick)

        threading.Thread(target=self.wait_for_my_turn).start()

    def relative_to_absolute(self, x: float, y: float):
        """
        Converts relative coordinates to absolute ones. Coordinates provided by mouse events are relative to the
        current zoom, so for some uses (like determining what tile has been clicked) they need to be scaled and shifted.
        """
        current = arcade.get_viewport()
        real_y = y * (current[3] - current[2]) / self.SCREEN_HEIGHT + current[2] - self.centering_y
        real_x = x * (current[1] - current[0]) / self.SCREEN_WIDTH + current[0] - self.centering_x
        return real_x, real_y

    def absolute_to_tiles(self, x: float, y: float):
        """
        Converts absolute coordinates to map matrix indices of the tile they lay on.
        """
        return map(lambda a: int(a // (self.tile_size + MARGIN)), (x, y))

    def get_tile(self, x, y):
        return self.tile_sprites[y * self.TILE_COLS + x]

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.top_bar.adjust()
        self.unit_popup.adjust()

    def on_hide_view(self):
        print("im hidden")

    def on_update(self, delta_time: float):
        self.game_logic.update()
        if self.update_popup:
            self.unit_popup.update()
            self.update_popup = False

    def on_draw(self):
        self.top_bar.turn_change(self.cur_enemy)
        arcade.start_render()
        # units, cities, move ranges
        self.game_logic.draw()
        # top bar
        self.top_bar.draw_background()
        # unit popup
        self.unit_popup.draw_background()
        self.city_popup.draw_background()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.city_popup.visible():
            return
        if 0 <= self.zoom + scroll_y < MAX_ZOOM:
            self.zoom += scroll_y
            current = arcade.get_viewport()

            new_width = (current[1] - current[0]) - 2 * scroll_y * self.SCROLL_STEP_X
            new_height = (current[3] - current[2]) - 2 * scroll_y * self.SCROLL_STEP_Y

            # we need to check if zooming will cross the borders of the map, if so - snap them back
            x, y = self.relative_to_absolute(x, y)
            new_left = x - new_width / 2
            if new_left > 0:
                x_shift = self.SCREEN_WIDTH - (new_left + new_width)
                if x_shift < 0:
                    new_left += x_shift
            else:
                new_left = 0

            new_bottom = y - new_height / 2
            if new_bottom > 0:
                # now, the size of the top bar changes and the zoom has to adjust
                # this means that in no zoom we can move closer to camera_top = screen_height than if we zoom in
                # and that's because the height of the top bar in pixels is the largest when zoomed out
                # actually, in no zoom we can move all the way up there
                # so the max camera_top for when zoomed in n times is:
                # screen_height - (max_top_bar_height - top_bar_height_after_zoom_change)
                y_shift = (self.SCREEN_HEIGHT - (self.zoom * 2 * self.SCROLL_STEP_Y) * self.top_bar.size_y) - (
                        new_bottom + new_height)
                if y_shift < 0:
                    new_bottom += y_shift
            else:
                new_bottom = 0

            arcade.set_viewport(new_left, new_left + new_width, new_bottom, new_bottom + new_height)
            self.top_bar.adjust()
            self.unit_popup.adjust()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.city_popup.visible():
            return
        if buttons == 4:
            current = arcade.get_viewport()
            # slow the movement down a lil bit
            dx /= 4
            dy /= 4

            if current[0] - dx < 0 or current[1] - dx > self.SCREEN_WIDTH:
                dx = 0
            # max_top = zoomed out map height + current top bar height,
            # cause we want to be able to see the edge of the map
            max_top = self.SCREEN_HEIGHT - self.top_bar.max_height + self.top_bar.height
            if current[2] - dy < 0 or current[3] - dy > max_top:
                dy = 0

            arcade.set_viewport(current[0] - dx, current[1] - dx, current[2] - dy, current[3] - dy)
            self.top_bar.adjust()
            self.unit_popup.adjust()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.city_popup.visible():
            return
        if button == 1:
            # don't let the player click through the unit pop-up or the top bar
            if self.unit_popup.is_hit(x, y) or self.top_bar.is_hit(x, y):
                pass
            else:
                # the x and y arguments are relative to the current zoom, so we need to scale and shift them
                x, y = self.relative_to_absolute(x, y)
                # aaand then turn them into grid coords
                tile_col, tile_row = self.absolute_to_tiles(x, y)

                # some fun stuff to do for testing, essentially a map editor tbh
                if tile_col < self.TILE_COLS and tile_row < self.TILE_ROWS:
                    # sprite list is 1d so we need to turn coords into a single index
                    tile = self.tile_sprites[tile_row * self.TILE_COLS + tile_col]

                    if tile.occupied():
                        unit = tile.occupant
                        # hide the range cause we might have clicked another unit while it was displayed
                        self.game_logic.hide_unit_range()
                        if self.my_turn and self.game_logic.is_unit_mine(unit):
                            # show me where can i move it
                            self.unit_popup.display(unit, mine=True)
                            self.game_logic.display_unit_range(unit)
                        else:
                            # just show the info
                            self.unit_popup.display(unit, mine=False)
                    elif self.unit_popup.visible():
                        unit = self.unit_popup.unit
                        cost = self.game_logic.can_unit_move(unit, tile_col, tile_row)
                        if self.my_turn and cost:
                            # if it's my turn and my unit and i clicked within its range, move it
                            self.client.move_unit(*unit.tile.coords, tile_col, tile_row, cost)
                            self.game_logic.move_unit(unit, tile_col, tile_row, cost)
                            self.unit_popup.update()
                        else:
                            # otherwise it means that i "unclicked" the popup
                            self.unit_popup.hide()
                            self.game_logic.hide_unit_range()
                    elif self.my_turn:
                        if tile.city:
                            self.window.show_view(CityView(tile.city, self.top_bar))  # TODO Gabi to tutaj
                        else:
                            self.game_logic.add_unit(tile_col, tile_row, self.client.nick, settler=True)
                            self.client.add_unit(tile_col, tile_row, "settler")

    def on_key_press(self, symbol, modifiers):
        if self.my_turn:
            if self.city_popup.visible():
                if symbol == arcade.key.ESCAPE:
                    self.city_popup.hide()
                elif symbol == arcade.key.ENTER:
                    city_name = self.city_popup.hide()
                    unit = self.unit_popup.unit
                    self.client.add_city(*unit.tile.coords, city_name)
                    self.game_logic.build_city(self.unit_popup.unit)
                    self.unit_popup.hide()
                    self.game_logic.hide_unit_range()
            else:
                # END TURN
                if symbol == arcade.key.SPACE:
                    self.my_turn = False
                    self.client.end_turn()
                    self.unit_popup.hide()
                    self.game_logic.end_turn()
                    threading.Thread(target=self.wait_for_my_turn, daemon=True).start()
                # BUILD A CITY
                elif symbol == arcade.key.N and self.unit_popup.can_build_city():
                    unit = self.unit_popup.unit
                    if self.game_logic.is_unit_mine(unit):
                        self.city_popup.display(unit)
                        return

    def wait_for_my_turn(self):
        """
        A prototype function for handling server messages about other players' actions. Will probably be renamed and
        maybe split later on.
        """
        while True:
            message = self.client.get_opponents_move()
            if message[0] == "TURN":
                if message[1] == self.client.nick:
                    self.my_turn = True
                    self.cur_enemy = ""
                    return
                else:
                    self.cur_enemy = message[1]

            elif message[0] == "ADD_UNIT":
                nick = message[1]
                x, y = eval(message[2])
                self.game_logic.add_unit(x, y, nick, message[3] == "settler")

            elif message[0] == "MOVE_UNIT":
                x0, y0 = eval(message[1])
                x1, y1 = eval(message[2])
                cost = int(message[3])
                self.game_logic.move_opponents_unit(x0, y0, x1, y1, cost)
                self.update_popup = True

            elif message[0] == "ADD_CITY":
                nick = message[1]
                x, y = eval(message[2])
                city_name = message[3]
                self.game_logic.build_opponents_city(x, y)
                self.unit_popup.hide_if_on_tile(x, y)

