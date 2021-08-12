import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLDEN = (184, 134, 11)
CRIMSON = (220, 20, 60)
CADETBLUE = (95, 158, 160)
LIGHTCYAN = (224, 255, 255)
KHAKI = (240, 230, 140)

score = 0
player_lives = 3
clock = pygame.time.Clock()
FPS = 10  # controls how often the screen should refresh.  It will refresh every 1/12th second

# entities in the game
fruits = ['orange', 'mango', 'pome', 'bomb', 'apple', 'tomato', 'strawberry', 'pumpkin', 'pineapple', 'melon']

# Game window width and height
(width, height) = (800, 498)
WIDTH = 800
HEIGHT = 498


# Screen declaration
Screen = pygame.display.set_mode((width, height))
Screen.fill(WHITE)


# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    fruit_path = "./photos/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        # where the fruit should be positioned on x-coordinate
        'x': random.randint(100, 500),
        'y': 800,

        # how fast the fruit should move in x direction. Controls the diagonal movement of fruits
        'speed_x': random.randint(-10, 10),
        # control the speed of fruits in y-direction ( UP )
        'speed_y': random.randint(-80, -60),
        # determines if the generated coordinate of the fruits is outside the gameDisplay or not. If outside,
        # then it will be discarded
        'throw': False,
        't': 0,
        'hit': False,
    }

    # Return the next random floating point number in the range [0.0, 1.0] to keep the fruits inside the gameDisplay
    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False


# Dictionary to hold the data the random fruit generation
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)


# helps to draw text on the screen
def draw_text(win, text, size, x, y, font_file='Avocado Creamy'):
    font_name = pygame.font.match_font(font_file)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    # draws image or writes text on the screen at a specified position
    win.blit(text_surface, text_rect)


def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 45 * i)
        img_rect.y = y
        display.blit(img, img_rect)


def hide_cross_lives(x, y):
    Screen.blit(pygame.image.load("./photos/red_lives.png"), (x, y))


# Button class
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # win = specify screen
    def draw(self, win, font_size, outline=None):
        # call this function to draw button on screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', font_size)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, posit):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < posit[0] < self.x + self.width:
            if self.y < posit[1] < self.y + self.height:
                return True
        return False


def MainWindow():
    pygame.display.set_caption("RPPOOP Project - FRUIT NINJA GAME")
    Screen.fill(CADETBLUE)
    # convert method used to create a copy that will draw more quickly on the screen
    background = pygame.image.load('./photos/name.jpg').convert()
    Screen.blit(background, (0, 50))
    StartGameButton.draw(Screen, 60, BLACK)
    pygame.display.update()


def GameWindow():
    global score, player_lives  # to save changes in score, player_lives
    Screen.fill(WHITE)
    background = pygame.image.load('./photos/woodBackground.jpg').convert()
    pygame.display.set_caption("FRUIT NINJA GAME")

    score = 0

    # blit stands for Block Transfer
    # copy the contents of one Surface to another
    Screen.blit(background, (0, 0))

    EndGameButton.draw(Screen, 70, BLACK)
    pygame.display.flip()
    draw_text(Screen, 'Score : ' + str(score), 60, 100, 10)

    first_round = True
    game_over = True
    game_running = True

    while game_running:
        if game_over:
            if first_round:
                first_round = False
            game_over = False
            player_lives = 3
            Screen.blit(background, (0, 0))
            EndGameButton.draw(Screen, 25, BLACK)
            score = 0
            draw_lives(Screen, 670, 110, player_lives, "./photos/red_lives.png")
            draw_text(Screen, 'Score : ' + str(score), 60, 100, 10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_running = False

            position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EndGameButton.isOver(position):
                    game_running = False

            # screen update
            Screen.blit(background, (0, 0))
            EndGameButton.draw(Screen, 25, BLACK)
            draw_text(Screen, 'Score : ' + str(score), 60, 100, 10)
            draw_lives(Screen, 670, 110, player_lives, './photos/red_lives.png')

            # loop for fruit generation and hit
            for key, value in data.items():
                # throw ensures that the fruit remains in display region
                if value['throw']:
                    # moving the fruits in x-coordinates
                    # modify position depending on speed
                    value['x'] += value['speed_x']
                    # moving the fruits in y-coordinate
                    value['y'] += value['speed_y']
                    # increasing y-coordinate for next iteration
                    value['speed_y'] += (1 * value['t'])
                    # increasing speed_y for next loop
                    value['t'] += 1

                    # displaying the fruit inside screen dynamically
                    if value['y'] <= 800:
                        # display fruit on screen
                        Screen.blit(value['img'], (value['x'], value['y']))
                    else:
                        generate_random_fruits(key)

                    # get current position of mouse
                    current_position = pygame.mouse.get_pos()

                    # hit conditions - slice conditions
                    # hit is initialised as  false
                    # not hit = true
                    # current_pos = [x,y] --> curr_pos[0] = x coordinate, curr_pos[1] = y coordinate
                    # size of fruit images is of dimensions 60 * 60 pixels
                    if not value['hit'] and value['x'] < current_position[0] < value['x'] + 80 \
                            and value['y'] < current_position[1] < value['y'] + 80:
                        # if condition true = player has hit a fruit or a bomb

                        # if a bomb is hit
                        if key == 'bomb':
                            player_lives -= 1

                            # if all 3 lives end
                            if player_lives == 0:
                                hide_cross_lives(670, 110)  # the all cross will disappear
                            elif player_lives == 1:
                                hide_cross_lives(715, 110)  # last two cross disappear
                            elif player_lives == 2:
                                hide_cross_lives(760, 110)  # only 3rd or last cross will disappear

                            # more than 3 times bomb has been hit - end game
                            if player_lives < 0:
                                show_gameover_screen(game_over)
                                game_over = True
                                game_running = False

                            # half bomb should be displayed
                            half_fruit_path = "./photos/explosion.png"

                        # key is not a bomb
                        else:
                            half_fruit_path = "./photos/" + "half_" + key + ".png"

                        # now the fruit is cut into half so change image
                        value['img'] = pygame.image.load(half_fruit_path)

                        # increase speed as the half fruit or bomb must go immediately from screen
                        value['speed_x'] += 10

                        # score update
                        if key != 'bomb':
                            score += 1
                        draw_text(Screen, 'Score : ' + str(score), 60, 100, 10)

                        # change hit parameter
                        value['hit'] = True
                else:
                    # if fruit or bomb was not hit
                    generate_random_fruits(key)

        pygame.display.update()
        clock.tick(FPS)  # reduces the speed of the loop


def show_gameover_screen(game_over):
    draw_text(Screen, "GAME OVER", 84, width / 2, height / 4)
    pygame.display.flip()
    if not game_over:
        draw_text(Screen, "Score : " + str(score), 60, width / 2, 220)
    draw_text(Screen, "PLAY AGAIN?", 64, width / 2, 300)
    YesButton.draw(Screen, 25, BLACK)
    NoButton.draw(Screen, 25, BLACK)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if EndGameButton.isOver(position):
                    print("End game button")
                    waiting = False

                if YesButton.isOver(position):
                    GameWindow()

                if NoButton.isOver(position):
                    waiting = False


# button declaration
StartGameButton = Button(CADETBLUE, 265, 370, 270, 100, 'Start Game')
EndGameButton = Button(KHAKI, 660, 25, 130, 60, "End Game")
YesButton = Button(LIGHTCYAN, 270, 360, 80, 40, " YES ")
NoButton = Button(LIGHTCYAN, 440, 360, 80, 40, " NO ")

# Main Loop of program
running = True
while running:
    MainWindow()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:  # until you close the window
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            if StartGameButton.isOver(pos):
                StartGameButton.color = GOLDEN
            else:
                StartGameButton.color = LIGHTCYAN

        if event.type == pygame.MOUSEBUTTONDOWN:
            if StartGameButton.isOver(pos):
                GameWindow()

pygame.quit()
