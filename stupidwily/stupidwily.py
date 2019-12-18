#!/usr/bin/env python3


import pyglet
import arcade


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
SCREEN_TITLE = "Mega Man: Dr. Wily's Stupid"
SCREEN_SCALE = 4

TILE_SIZE = 16

PLAYER_MOVEMENT_SPEED = 2
PLAYER_JUMP_SPEED = 10
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
        
        # Setup the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()
        
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)

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

def main():
    window = StupidGame()
    window.setup()
    
    # Start the game!
    arcade.run()

if __name__ == "__main__":
    main()
