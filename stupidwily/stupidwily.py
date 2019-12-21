#!/usr/bin/env python3


import pyglet
import arcade


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Mega Man: Dr. Wily's Stupid"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = (1024 / 2) - (84 / 2)
RIGHT_VIEWPORT_MARGIN = (1024 / 2) - (84 / 2)

TILE_SIZE = 64

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1


class StupidGame(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, antialiasing=False)
        
        # Hide the mouse cursor
        self.set_mouse_visible(False)
        
        # Initialize sprite lists
        self.player_list = None
        self.wall_list = None
        
        # Initialize sprites
        self.player_sprite = None

        # Used to keep track of our scrolling
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.LIGHT_CYAN)

    def setup(self):
        # Setup sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        
        # Setup player sprite
        self.player_sprite = arcade.Sprite("images/hero-standing-01.png")
        self.player_sprite.center_x = self.player_sprite.width // 2
        self.player_sprite.center_y = self.player_sprite.height // 2
        self.player_sprite.position = (100, 100)
        self.player_list.append(self.player_sprite)
        
        for x in range(0, SCREEN_WIDTH * 16, TILE_SIZE):
            wall_sprite = arcade.Sprite("images/tile-gray-01.png")
            wall_sprite.position = (x, 0)
            self.wall_list.append(wall_sprite)
        
        for x in range(TILE_SIZE * 4, TILE_SIZE * 8, TILE_SIZE):
            wall_sprite = arcade.Sprite("images/tile-gray-01.png")
            wall_sprite.position = (x, TILE_SIZE * 2)
            self.wall_list.append(wall_sprite)
        
        # Setup the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()
        
        # Draw sprites
        self.player_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()

        # Manage scrolling

        # Track if we need to change the viewport
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, 0, SCREEN_HEIGHT)

def main():
    window = StupidGame()
    window.setup()
    
    # Start the game!
    arcade.run()

if __name__ == "__main__":
    main()
