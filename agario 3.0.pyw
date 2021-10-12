import arcade
import random
import time

# задаем ширину, высоту и заголовок окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Circle Game"

class OurGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)
        self.circles=arcade.SpriteList()
        self.player = None
        self.is_pause = True
        self.text = ""
        self.text_lose=""
        self.text_phase_shift="Aviable"
        self.is_game = True
        self.phase_shift = False
        self.timer=0
        self.cd=0
        self.phase_shift_aviable=True
        self.kill_all=True
        self.first_time=True
        

        self.sound = arcade.load_sound('Sounds/Drip Drop.wav')
        self.inv_sound=arcade.load_sound("Sounds/inv.mp3")
        self.kill_all_sound=arcade.load_sound("Sounds/kill_all.mp3")
        self.nyam_sound=arcade.load_sound("Sounds/nyam.mp3")
        self.lose_sound=arcade.load_sound("Sounds/lose.mp3")
        self.start_sound=arcade.load_sound("Sounds/start.mp3")

# начальные значения
    def setup(self):
        
        self.music = arcade.play_sound(self.sound)
        self.sound.set_volume(0.1, self.music)
        
        self.player = Player()
        for i in range(30):
            circle=Circle(random.uniform(0.1, self.player.scale + 0.5))
            self.circles.append(circle)

    # отрисовка объектов
    def on_draw(self):
        arcade.start_render()
        self.circles.draw()
        self.player.draw()
        
        arcade.draw_text("Pause: Mouse click", 50, self.height - 50, arcade.color.WHITE)
        arcade.draw_text("Exit: Esc", self.width - 100, self.height - 50, arcade.color.WHITE)

        if self.phase_shift_aviable:
            arcade.draw_text("Space for 3s invulnerability: " + self.text_phase_shift, 50, 20, arcade.color.WHITE)
        else:
            arcade.draw_text("Space for 3s invulnerability: " + str(round(self.cd)), 50, 20, arcade.color.WHITE)
            

        
        arcade.draw_text(self.text, (self.width / 2) - 100, self.height / 2, arcade.color.WHITE, 80)
        arcade.draw_text(self.text_lose, (self.width / 2) - 300, self.height / 2, arcade.color.WHITE, 80)

    # логика
    def update(self, delta_time):
        
        if not self.is_pause and self.is_game:
            if self.sound.get_stream_position(self.music) == 0:
                self.music = arcade.play_sound(self.sound)
                self.sound.set_volume(0.1, self.music)
            
            while len(self.circles) < 30:
                circle = Circle(random.uniform(0.1, self.player.scale + 0.5))
                self.circles.append(circle)

            self.circles.update()
            self.player.update()
            
            collisions = arcade.check_for_collision_with_list(self.player, self.circles)
            if len(collisions) > 0:
                for circle in collisions:
                    if circle.scale > self.player.scale and self.phase_shift!=True:
                        
                        self.is_game=False
                        self.text_lose="Press R to restart"
                        arcade.play_sound(self.lose_sound)
                        time.sleep(2)
                    else:
                        if self.phase_shift!=True:
                            self.player.scale += 0.01
                            arcade.play_sound(self.nyam_sound)
                            circle.kill()
                        if self.player.scale >= 2:
                            self.is_game=False
                            self.text="YOU WIN!"

        if not self.is_game:
            self.player.kill()
            for circle in self.circles:
                circle.kill()

        if self.timer>0:
            self.timer-=0.05
            self.player.color=255,204,0
        if self.timer<=0:
            self.phase_shift=False
            self.player.color=255,255,255

        if self.cd>0:
            self.cd-=0.05
            self.phase_shift_aviable=False
        if self.cd<=0:
            self.phase_shift_aviable=True
        
            


    def on_mouse_motion(self, x, y, dx, dy):
        if not self.is_pause:
            self.player.center_x = x
            self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_game:
            if self.is_pause:
                if self.first_time:
                    arcade.play_sound(self.start_sound)
                    time.sleep(1.5)
                    self.first_time=False
                
                self.is_pause = False
                self.set_mouse_visible(False)
                self.text = ""

            else:
                self.is_pause = True
                self.set_mouse_visible(True)
                self.text = "Pause"


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            window.close()
        if key == arcade.key.SPACE and self.is_game and self.is_pause!=True and self.phase_shift_aviable:
            self.phase_shift=True
            arcade.play_sound(self.inv_sound)
            self.timer=5
            self.cd=10

        if key==arcade.key.F and self.kill_all and self.is_game and self.is_pause!=True:
            self.kill_all=False
            arcade.play_sound(self.kill_all_sound)
            time.sleep(2)
            for circle in self.circles:
                circle.kill()
                self.player.scale+=0.01
                
        #restart#    
        if key == arcade.key.R and self.is_game==False:
            
            arcade.play_sound(self.start_sound)
            time.sleep(1.5)
            
            self.is_game=True
            self.kill_all=True
            self.text_lose=""
            self.player = Player()
            self.player.center_x = window.width / 2
            self.player.center_y = window.height / 2
            self.player.scale = 0.3
            self.phase_shift = False
            self.timer=0
            self.cd=0
            self.phase_shift_aviable=True
            for circle in self.circles:
                circle.kill()
            
            

class Circle(arcade.Sprite):
    def __init__(self,scale):
        super().__init__('circle.png',scale)
        
        sides = ['left', 'top', 'right', 'bottom']
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.side = random.choice(sides)

        if self.side == 'left':
            self.right = 0
            self.center_y = random.randint(0, window.height)
            self.change_x = random.uniform(2, 5)
            self.change_y = random.uniform(-3, -2)
        elif self.side == 'top':
            self.bottom = window.height
            self.center_x = random.randint(0, window.width)
            self.change_y = random.uniform(-5, -2)
            self.change_x = random.uniform(-3, -2)
        elif self.side == 'right':
            self.left = window.width
            self.center_y = random.randint(0, window.height)
            self.change_x = random.uniform(-3, -2)
            self.change_y = random.uniform(-3, -2)
        else:
            self.top = 0
            self.center_x = random.randint(0, window.width)
            self.change_y = random.uniform(2, 3)
            self.change_x = random.uniform(-3, -2)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.side == 'left':
            if self.left >= window.width or self.top <= 0 or self.bottom >= window.height:
                self.kill()
                
        elif self.side == 'top':
            if self.top <= 0 or self.left >= window.width or self.right <= 0:
                self.kill()
                
        elif self.side == 'right':
            if self.right <= 0 or self.top <= 0 or self.bottom >= window.height:
                self.kill()
                
        else:
            if self.bottom >= window.height or self.left >= window.width or self.right <= 0:
                self.kill()


class Player(Circle):
    def __init__(self):
        super().__init__(0.3)
        self.center_x = window.width / 2
        self.center_y = window.height / 2
        self.change_x = 0
        self.change_y = 0

        self.color = 255,255,255


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
