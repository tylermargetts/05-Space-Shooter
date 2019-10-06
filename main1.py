"""
Move with a Sprite Animation

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_animation
"""
import arcade
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"

NUM_ENEMIES = 5
STARTING_LOCATION = (750,300)
BULLET_DAMAGE = 10
ENEMY_HP = 20
HIT_SCORE = 10
KILL_SCORE = 100

MOVEMENT_SPEED = 5

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/laser.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/Spaceship.png", 0.25)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
    
        super().__init__("assets/RightRun1.png", 0.75)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.score = 0
        self.enemy = None

        self.set_mouse_visible(False)
        
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0 

        self.background = None 

    def setup(self):
        self.enemy_list = arcade.SpriteList()

        # Set up the players
        self.score = 0
        self.enemy = arcade.AnimatedWalkingSprite()

        character_scale = 0.75
        self.enemy.stand_right_textures = []
        self.enemy.stand_right_textures.append(arcade.load_texture("assets/RightRun3.png",
                                                                    scale=character_scale))
        self.enemy.stand_left_textures = []
        self.enemy.stand_left_textures.append(arcade.load_texture("assets/RightRun3.png",
                                                                   scale=character_scale, mirrored=True))

        self.enemy.walk_right_textures = []

        self.enemy.walk_right_textures.append(arcade.load_texture("assets/RightRun1.png",
                                                                   scale=character_scale))
        self.enemy.walk_right_textures.append(arcade.load_texture("assets/RightRun2.png",
                                                                   scale=character_scale))
        self.enemy.walk_right_textures.append(arcade.load_texture("assets/RightRun3.png",
                                                                   scale=character_scale))
        self.enemy.walk_right_textures.append(arcade.load_texture("assets/RightRun3.png",
                                                                   scale=character_scale))

        

        self.enemy.texture_change_distance = 20
        self.enemy.scale = 0.8

        self.enemy.change_x = MOVEMENT_SPEED

        for i in range(NUM_ENEMIES):
            x = 50
            y = random.randrange(0, 500)
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy) 
        
        # Set the background color
        self.background = arcade.load_texture("assets/background.png")

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.enemy.change_x = MOVEMENT_SPEED

    def on_draw(self):
    
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def update(self, delta_time):
        """ Movement and game logic """
        self.bullet_list.update()
        import time
        import sys
        for e in self.enemy_list:
            collisions = e.collides_with_list(self.bullet_list)
            for c in collisions:
                c.kill()
                self.score += 10
                e.hp -= 10
            if e.hp <= 0:
                e.kill()
                self.score += 100
            if self.score >= 600:
                sys.exit()
                

        self.enemy_list.update()
        self.enemy_list.update_animation()

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_y = y

        # Generate a list of all sprites that collided with the player.
       

        # Loop through each colliding sprite, remove it, and add to the score.

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x - 50
            y = self.player.center_y 
            bullet = Bullet((x,y),(-10,0),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()