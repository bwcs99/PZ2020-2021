import arcade
import arcade.gui

TOP_BAR_SIZE = 0.0625  # expressed as the percentage of the current screen height
SCROLL_STEP = 0.125  # new_height = old_height +- 2 * scroll_step * original_height, same with width
MAX_ZOOM = int(1 / (2 * SCROLL_STEP))

TILE_ROWS = 25
TILE_COLS = 40
MARGIN = 1  # space between two tiles (vertically & horizontally) in pixels


class TopBar(arcade.gui.UIManager):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.width = screen_width
        self.height = TOP_BAR_SIZE * screen_height
        self.coords_lrtb = (0, screen_width, screen_height, screen_height - self.height)
        arcade.gui.elements.UIStyle.set_class_attrs(arcade.gui.elements.UIStyle.default_style(), "label", font_name="SUBWT", font_color=arcade.color.WHITE)

        self.money_label = Label("Treasury: 0 (+0)", 0, 0)
        self.time_label = Label("Press SPACE to end turn (5:00)", 0, 0)
        self.move(0, screen_width, 0, screen_height)
        self.add_ui_element(self.money_label)
        self.add_ui_element(self.time_label)

    def move(self, left, right, bottom, top):
        self.width = right - left
        self.height = TOP_BAR_SIZE * (top - bottom)
        self.coords_lrtb = (left, right, top, top - self.height)
        self.money_label.center_y = self.time_label.center_y = top - self.height / 2
        self.money_label.height = self.time_label.height = 0.8 * self.height
        self.money_label.center_x = left + 0.125 * self.width
        self.time_label.center_x = left + 0.775 * self.width
        self.money_label.width = 0.2 * self.width
        self.time_label.width = 0.4 * self.width

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass


class Label(arcade.gui.UILabel):
    def __init__(self, text, center_x, center_y):
        super().__init__(text, center_x, center_y)


"""
class TopBar:
    def __init__(self, screen_width, screen_height):
        self.coords_lrtb = (0, screen_width, screen_height, (1 - TOP_BAR_SIZE) * screen_height)
        self.width = screen_width
        self.height = TOP_BAR_SIZE * screen_height
        self.money_text_args = 0.1 * self.width, screen_height - 0.9 * self.height, arcade.color.PEACH

    def move(self, left, right, bottom, top):
        self.width = right - left
        self.height = TOP_BAR_SIZE * (top - bottom)
        self.coords_lrtb = (left, right, top, top - self.height)
        self.money_text_args = left + 0.1 * self.width, top - 0.9 * self.height, arcade.color.PEACH
"""

class GameView(arcade.View):
    def __init__(self, width, height):
        super().__init__()

        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.SCROLL_STEP_X = SCROLL_STEP * width
        self.SCROLL_STEP_Y = SCROLL_STEP * height
        self.zoom = 0

        self.top_bar = TopBar(width, height)

        self.tiles = [[0 for _ in range(TILE_COLS)] for _ in range(TILE_ROWS)]
        self.tile_sprites = arcade.SpriteList()
        # needs to be smarter but depends on the size of a real map tbh
        self.tile_size = int(((1 - TOP_BAR_SIZE) * height) / TILE_ROWS) - MARGIN
        # in order to center the tiles vertically and horizontally
        self.centering_x = (width - TILE_COLS * (self.tile_size + MARGIN)) / 2
        self.centering_y = ((1 - TOP_BAR_SIZE) * height - TILE_ROWS * (self.tile_size + MARGIN)) / 2

        for row in range(TILE_ROWS):
            for col in range(TILE_COLS):
                tile = arcade.SpriteSolidColor(self.tile_size, self.tile_size, arcade.color.WHITE)
                tile.center_x = col * (self.tile_size + MARGIN) + (self.tile_size / 2) + MARGIN + self.centering_x
                tile.center_y = row * (self.tile_size + MARGIN) + (self.tile_size / 2) + MARGIN + self.centering_y
                tile.color = arcade.color.BABY_BLUE
                self.tile_sprites.append(tile)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.top_bar.move(*arcade.get_viewport())

    def on_draw(self):
        arcade.start_render()
        self.tile_sprites.draw()
        current = arcade.get_viewport()
        # top bar
        arcade.draw_lrtb_rectangle_filled(*self.top_bar.coords_lrtb, arcade.color.ST_PATRICK_BLUE)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if 0 <= self.zoom + scroll_y < MAX_ZOOM:
            self.zoom += scroll_y
            current = arcade.get_viewport()

            new_width = (current[1] - current[0]) - 2 * scroll_y * self.SCROLL_STEP_X
            new_height = (current[3] - current[2]) - 2 * scroll_y * self.SCROLL_STEP_Y

            # we need to check if zooming will cross the borders of the map, if so - snap them back
            new_left = current[0] + scroll_y * self.SCROLL_STEP_X
            if new_left > 0:
                x_shift = self.SCREEN_WIDTH - (new_left + new_width)
                if x_shift < 0:
                    new_left += x_shift
            else:
                new_left = 0

            new_bottom = current[2] + scroll_y * self.SCROLL_STEP_Y
            if new_bottom > 0:
                # now, the size of the top bar changes and the zoom has to adjust
                # this means that in no zoom we can move closer to camera_top = screen_height than if we zoom in
                # and that's because the height of the top bar in pixels is the largest when zoomed out
                # actually, in no zoom we can move all the way up there
                # so the max camera_top for when zoomed in n times is:
                # screen_height - (max_top_bar_height - current_top_bar_height)
                y_shift = (self.SCREEN_HEIGHT - (self.zoom * 2 * self.SCROLL_STEP_Y) * TOP_BAR_SIZE) - (
                        new_bottom + new_height)
                if y_shift < 0:
                    new_bottom += y_shift
            else:
                new_bottom = 0

            self.top_bar.move(new_left,
                              new_left + new_width,
                              new_bottom,
                              new_bottom + new_height
                              )

            arcade.set_viewport(
                new_left,
                new_left + new_width,
                new_bottom,
                new_bottom + new_height
            )

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == 4:
            current = arcade.get_viewport()
            if current[0] - dx < 0 or current[1] - dx > self.SCREEN_WIDTH:
                dx = 0
            # max_top = zoomed out map height + current top bar height,
            # cause we want to be able to see the edge of the map
            max_top = (1 - TOP_BAR_SIZE) * self.SCREEN_HEIGHT + self.top_bar.height
            if current[2] - dy < 0 or current[3] - dy > max_top:
                dy = 0
            self.top_bar.move(current[0] - dx, current[1] - dx, current[2] - dy, current[3] - dy)
            arcade.set_viewport(
                current[0] - dx, current[1] - dx, current[2] - dy, current[3] - dy,
            )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            current = arcade.get_viewport()
            # the x and y argument are relative to the current zoom, so we need to scale and shift them
            # and also not let the player click on tiles through the top bar
            real_y = y * (current[3] - current[2]) / self.SCREEN_HEIGHT + current[2] - self.centering_y
            if real_y < current[3] - self.top_bar.height:
                real_x = x * (current[1] - current[0]) / self.SCREEN_WIDTH + current[0] - self.centering_x
                # aaand then turn them into grid coords
                tile_col = int(real_x // (self.tile_size + MARGIN))
                tile_row = int(real_y // (self.tile_size + MARGIN))

                # some fun stuff to do for testing, essentially a map editor tbh
                if tile_col < TILE_COLS and tile_row < TILE_ROWS:
                    self.tiles[tile_row][tile_col] += 1
                    self.tiles[tile_row][tile_col] %= 4
                    color = self.tiles[tile_row][tile_col]
                    if color == 0:
                        color = arcade.color.BABY_BLUE
                    elif color == 1:
                        color = arcade.color.BUD_GREEN
                    elif color == 2:
                        color = arcade.color.EARTH_YELLOW
                    else:
                        color = arcade.color.RED_BROWN

                    # sprite list is 1d so we need to turn coords into a single index
                    self.tile_sprites[tile_row * TILE_COLS + tile_col].color = color
