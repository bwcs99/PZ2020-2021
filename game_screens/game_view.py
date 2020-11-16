import arcade
import arcade.gui
import threading
from time import sleep

TOP_BAR_SIZE = 0.0625  # expressed as the percentage of the current screen height

SCROLL_STEP = 0.125  # new_height = old_height +- 2 * scroll_step * original_height, same with width
MAX_ZOOM = int(1 / (2 * SCROLL_STEP))

# TILE_ROWS = 25
# TILE_COLS = 40
MARGIN = 1  # space between two tiles (vertically & horizontally) in pixels (while fully zoomed out)


class TopBar(arcade.gui.UIManager):
    """
    A representation of the game window's top bar containing info about the player's treasury and the name of the
    player whose turn is currently taking place. Holds and updates the current position of the bar on the screen.
    """

    def __init__(self, screen_width: int, screen_height: int, size: float = TOP_BAR_SIZE):
        """
        :param size: Should be between 0 and 1. Determines what part of the current screen height should the bar occupy.
        """
        super().__init__()

        self.width = screen_width
        self.size = size
        self.max_height = self.height = size * screen_height
        self.coords_lrtb = (0, screen_width, screen_height, screen_height - self.height)

        # this can go into a file later maybe
        arcade.gui.elements.UIStyle.set_class_attrs(
            arcade.gui.elements.UIStyle.default_style(),
            "label",
            font_name="resources/fonts/november",
            font_color=arcade.color.WHITE,
            font_size=64
        )

        self.money_label = arcade.gui.UILabel("Treasury: 0 (+0)", 0, 0)
        self.time_label = arcade.gui.UILabel("Press SPACE to end turn (5:00)", 0, 0)
        self.adjust()
        self.add_ui_element(self.money_label)
        self.add_ui_element(self.time_label)

    def adjust(self):
        """
        Adjusts the coords of the bar and it's elements to the current screen borders.
        """
        left, right, bottom, top = arcade.get_viewport()
        self.width = right - left
        self.height = self.size * (top - bottom)
        self.coords_lrtb = (left, right, top, top - self.height)
        # prosze pana ale niech pan to zrobi porzadnie
        self.money_label.center_y = self.time_label.center_y = top - self.height / 2
        self.money_label.height = self.time_label.height = 0.4 * self.height
        self.money_label.center_x = left + 0.125 * self.width
        self.time_label.center_x = left + 0.775 * self.width
        self.money_label.width = len(self.money_label.text) / 75 * self.width
        self.time_label.width = len(self.time_label.text) / 75 * self.width

    def turn_change(self, nick: str = None):
        """
        Changes the label to reflect the player whose turn is taking place. No nick should be provided if it's the
        turn of the player running the client.
        """
        if nick:
            self.time_label.text = f"{nick}'s turn (5:00)"
        else:
            self.time_label.text = "Press SPACE to end turn (5:00)"
        self.adjust()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, button, modifiers):
        pass


class Tile(arcade.SpriteSolidColor):
    """
    Represents a single square map tile. Has the ability to hold information about the potential unit occupying it.
    """

    def __init__(self, size: int):
        super().__init__(size, size, arcade.color.WHITE)
        self.occupant = None

    def occupied(self):
        return bool(self.occupant)


class GameView(arcade.View):
    """
    The view of the map of the game.
    """

    def __init__(self, width: int, height: int, tiles: list):
        """
        :param width: Max screen width.
        :param height: Max screen height.
        :param tiles: A 2D list of integer values representing tile types.
        """
        super().__init__()
        self.my_turn = True
        self.cur_enemy = ""

        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.SCROLL_STEP_X = SCROLL_STEP * width
        self.SCROLL_STEP_Y = SCROLL_STEP * height
        self.TILE_ROWS = len(tiles)
        self.TILE_COLS = len(tiles[0])
        self.zoom = 0

        self.top_bar = TopBar(width, height)

        self.tiles = tiles
        tile_types = [
            (0, 64, 128),
            (112, 169, 0),
            (16, 128, 64),
            (128, 128, 128)
        ]
        self.tile_sprites = arcade.SpriteList()
        # needs to be smarter tbh but depends on the size of a real map
        self.tile_size = int((height - self.top_bar.height) / self.TILE_ROWS) - MARGIN
        # in order to center the tiles vertically and horizontally
        self.centering_x = (width - self.TILE_COLS * (self.tile_size + MARGIN)) / 2
        self.centering_y = ((height - self.top_bar.height) - self.TILE_ROWS * (self.tile_size + MARGIN)) / 2

        for row in range(self.TILE_ROWS):
            for col in range(self.TILE_COLS):
                tile = Tile(self.tile_size)
                tile.color = tile_types[tiles[row][col]]  # can and will be changed to sprites as soon as we have em
                tile.center_x = col * (self.tile_size + MARGIN) + (self.tile_size / 2) + MARGIN + self.centering_x
                tile.center_y = row * (self.tile_size + MARGIN) + (self.tile_size / 2) + MARGIN + self.centering_y
                self.tile_sprites.append(tile)

        # this is ugly but she's moving out soon i promise
        self.unit_sprites = arcade.SpriteList()
        unit_prototype = arcade.Sprite(":resources:images/items/star.png")
        unit_prototype.height = unit_prototype.width = self.tile_size
        col, row = self.absolute_to_tiles(100, 100)
        self.place_unit_on_tile(unit_prototype, col, row)
        self.unit_sprites.append(unit_prototype)

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

    def place_unit_on_tile(self, unit: arcade.Sprite, col: int, row: int):
        """
        Places the provided unit on the tile identified by the map matrix coordinates.
        """
        tile = self.tile_sprites[row * self.TILE_COLS + col]
        unit.center_x = tile.center_x
        unit.center_y = tile.center_y
        tile.occupant = unit

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.top_bar.adjust()

    def on_draw(self):
        self.top_bar.turn_change(self.cur_enemy)
        arcade.start_render()
        self.tile_sprites.draw()
        self.unit_sprites.draw()
        # top bar
        arcade.draw_lrtb_rectangle_filled(*self.top_bar.coords_lrtb, arcade.color.ST_PATRICK_BLUE)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
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
                y_shift = (self.SCREEN_HEIGHT - (self.zoom * 2 * self.SCROLL_STEP_Y) * self.top_bar.size) - (
                        new_bottom + new_height)
                if y_shift < 0:
                    new_bottom += y_shift
            else:
                new_bottom = 0

            arcade.set_viewport(new_left, new_left + new_width, new_bottom, new_bottom + new_height)
            self.top_bar.adjust()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
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

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1 and self.my_turn:
            # the x and y argument are relative to the current zoom, so we need to scale and shift them
            x, y = self.relative_to_absolute(x, y)
            # and also not let the player click on tiles through the top bar
            if y < arcade.get_viewport()[3] - self.top_bar.height:
                # aaand then turn them into grid coords
                tile_col, tile_row = self.absolute_to_tiles(x, y)

                # some fun stuff to do for testing, essentially a map editor tbh
                if tile_col < self.TILE_COLS and tile_row < self.TILE_ROWS:
                    # sprite list is 1d so we need to turn coords into a single index
                    tile = self.tile_sprites[tile_row * self.TILE_COLS + tile_col]

                    if tile.occupied():
                        print("There's a unit here!")
                    else:
                        self.tiles[tile_row][tile_col] += 1
                        self.tiles[tile_row][tile_col] %= 4
                        color = self.tiles[tile_row][tile_col]
                        if color == 0:
                            color = (0, 64, 128)
                        elif color == 1:
                            color = (112, 169, 0)
                        elif color == 2:
                            color = (16, 128, 64)
                        else:
                            color = (128, 128, 128)
                        tile.color = color

    def on_key_press(self, symbol, modifiers):
        if symbol == ord(" "):
            print("end")
            # TODO: use client to send the message to server
            # get an answer about ending successfully, preferably
            # and then learn whose turn it is now
            self.my_turn = False
            threading.Thread(target=self.wait_for_my_turn).start()

    def wait_for_my_turn(self):
        """
        A prototype function for handling server messages. Will probably be renamed and split later on.
        """
        # TODO: Actual server communication
        message = "next_p"
        while message != "next":
            self.cur_enemy = message
            sleep(1)
            message = message[:-1]
        self.my_turn = True
        self.cur_enemy = ""
