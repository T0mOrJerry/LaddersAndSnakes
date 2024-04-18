# Preparing PyGame module to run the application
import pygame
import random

pygame.init()
running = True
clock = pygame.time.Clock()
FPS = 60

# Initializing constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
keys_codes = {48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 97: 'a',
              98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k',
              108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
              118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}
colors = [[(237, 152, 152), (222, 35, 35)], [(189, 152, 237), (116, 35, 222)], [(152, 170, 237), (35, 76, 222)],
          [(152, 237, 237), (35, 222, 222)], [(152, 237, 196), (35, 222, 132)],
          [(169, 237, 152), (73, 222, 35)], [(220, 237, 152), (185, 222, 35)],
          [(237, 229, 152), (222, 203, 35)], [(237, 203, 152), (222, 147, 35)],
          [(237, 187, 152), (222, 113, 35)], [(237, 162, 152), (222, 57, 35)]]
BigFont = pygame.font.SysFont("Arial", 60)
NormalFont = pygame.font.SysFont("Arial", 32)
TitleFont = pygame.font.SysFont("Arial", 100)
body_font = pygame.font.SysFont("Arial", 25)

# Omar
# Storing player data
players = {
    "Omar": [52, 820],
    "Alex": [63, 760],
    "Wilson": [54, 700]
}
plylist = list(players.keys())

# Alex
# Creating different surfaces for different purpose
# One general and one for each window
main_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
menu_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
guide_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
leader_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
choice_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Queue:
    def __init__(self):
        self.items = []
        self.ln = 0

    def enqueue(self, val):
        self.items.insert(0, val)

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        return ', '.join(list(map(str, self.items)))

    def size(self):
        return len(self.items)

    def __iter__(self):
        self.ln = self.size()
        return self

    def __next__(self):
        if self.ln <= 0:
            raise StopIteration
        self.ln -= 1
        return self.items[self.ln]


# Each window is described as a class, which draws everything, that must be drawn
# and helps to connect user and every interactive piece of the window
#########################################################################################
#########################################################################################
class Menu:
    def __init__(self):
        self.surface = menu_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.buttons = [
            StartButton(self.surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 7 * 4,
                        (102, 61, 14),
                        (227, 190, 148), 'Start'),
            BoardButton(self.surface, WINDOW_WIDTH / 3.5, WINDOW_HEIGHT / 8, WINDOW_WIDTH / 11,
                        WINDOW_HEIGHT / 7 * 5.045, (102, 61, 14),
                        (227, 190, 148), 'Leaderboard'),
            GuideButton(self.surface, WINDOW_WIDTH / 3.5, WINDOW_HEIGHT / 8, WINDOW_WIDTH / 8 * 5,
                        WINDOW_HEIGHT / 7 * 3.08, (102, 61, 14),
                        (227, 190, 148), 'User Guide'),
            ExitAppButton(self.surface, WINDOW_WIDTH / 6, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 50 - 20,
                          WINDOW_HEIGHT / 40 * 34 + 2,
                          (102, 17, 17),
                          (227, 190, 148), 'Exit the game'),
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
        self.surface.fill('white')
        btn_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


class Choice:
    def __init__(self):
        self.surface = guide_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.player_number = 1
        self.buttons = [
            ArrowUpButton(self.surface, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4,
                          WINDOW_HEIGHT / 7 * 4 - 20,
                          (102, 61, 14),
                          (227, 190, 148)),
            ArrowDownButton(self.surface, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4,
                            WINDOW_HEIGHT / 7 * 4 + 20,
                            (102, 61, 14),
                            (227, 190, 148)),
            ExitButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 44 * 39,
                       WINDOW_HEIGHT / 40 * 35,
                       (102, 17, 17),
                       (227, 190, 148), 'Exit'),
            ChoiceSubmitButton(self.surface, WINDOW_WIDTH / 14 * 3, WINDOW_HEIGHT / 14 * 2, WINDOW_WIDTH / 28 * 17,
                               WINDOW_HEIGHT / 14 * 7,
                               (26, 107, 39),
                               (227, 190, 148), 'Submit'),
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
        self.surface.fill('white')
        page_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render("Choose amount of players", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (WINDOW_WIDTH / 7 * 3, WINDOW_HEIGHT / 7 * 3, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7 * 2),
                         width=5)
        counter_txt = TitleFont.render(f"{self.player_number}", True, "Black", None)
        r = counter_txt.get_rect()
        self.surface.blit(counter_txt, (WINDOW_WIDTH / 7 * 3 + (WINDOW_WIDTH / 7 - r.width) / 2,
                                        WINDOW_HEIGHT / 7 * 3 + (WINDOW_HEIGHT / 7 * 2 - r.height) / 2))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


class Names:
    def __init__(self):
        self.surface = guide_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.buttons = [
            ExitButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 44 * 39,
                       WINDOW_HEIGHT / 40 * 35,
                       (102, 17, 17),
                       (227, 190, 148), 'Exit'),
            NamesSubmitButton(self.surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 9, WINDOW_WIDTH / 4,
                              WINDOW_HEIGHT / 5 * 2 + WINDOW_HEIGHT / 9 * 4,
                              (26, 107, 39),
                              (227, 190, 148), 'Submit'),
        ]
        self.fields = []
        for i in range(choice.player_number):
            self.fields.append(EnterField(self.surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 4,
                                          WINDOW_HEIGHT / 5 * 2 + WINDOW_HEIGHT / 9 * i))
        self.same_name_error = False

    # This function draws everything, which will be on the screen
    def draw(self):
        self.surface.fill('white')
        page_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render("Enter name(s) of player(s)", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        if self.same_name_error:
            warning_txt = NormalFont.render("All names must be different", True, "Red", None)
            r = warning_txt.get_rect()
            self.surface.blit(warning_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 3 + 5))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()
        for field in self.fields:
            field.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)
        for field in self.fields:
            field.check(user_event)

    def inp(self, user_event):  # Execute every user request
        for field in self.fields:
            field.inp(user_event)


class Guide:
    def __init__(self):
        self.surface = guide_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.buttons = [
            StartButton(self.surface, 0, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 7 * 4,
                        (0, 61, 14),
                        (227, 190, 148), 'Start'),
            ExitButton(self.surface, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4, WINDOW_WIDTH / 2,
                       WINDOW_HEIGHT / 7 * 5,
                       (102, 17, 17),
                       (227, 190, 148), 'Exit'),
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
        self.surface.fill('white')
        btn_txt = TitleFont.render("Guide", True, "Black", None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


# Omar
class Leaderboard:
    def __init__(self):
        self.surface = guide_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.buttons = [
            ExitButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 44 * 39,
                       WINDOW_HEIGHT / 40 * 35,
                       (102, 17, 17),
                       (227, 190, 148), 'Exit'),
        ]
        self.bodyheight = body_font.size("Body")[1]

    def add_text(self, txt, wid, hig, color=(227, 190, 148)):
        body_surface = body_font.render(str(txt), True, color)
        self.surface.blit(body_surface, (wid, hig))

    def result(self, li, di, i, y):  # maximum 7 players at one time
        pygame.draw.line(self.surface, (102, 61, 14), (0, y), (WINDOW_WIDTH, y), 50)
        self.add_text(str(i + 1), 0, y + self.bodyheight / 2 - 25)
        self.add_text(str(li[i]), WINDOW_WIDTH / 4 - 100, y + self.bodyheight // 2 - 25)
        self.add_text(str(di[li[i]][0]), WINDOW_WIDTH / 2 - 100, y + self.bodyheight / 2 - 25)
        self.add_text(str(di[li[i]][1]), WINDOW_WIDTH - 100, y + self.bodyheight / 2 - 25)

    def draw(self):
        self.surface.fill('white')
        # Omar, Create a surface that hold the title
        title_surface = TitleFont.render('Leaderboard', True, (0, 0, 0))
        # Blit the title surface onto the screen
        self.surface.blit(title_surface,
                          (WINDOW_WIDTH / 2 - TitleFont.size("Leaderboard")[0] / 2, WINDOW_HEIGHT / 50 - 20))
        # variable x equal to 0
        x = 200
        # adding subtitles
        self.add_text("Rank", 0, 125, (0, 0, 0))
        self.add_text("Name", WINDOW_WIDTH // 4 - 100, 125, (0, 0, 0))
        self.add_text("Number of Turns", WINDOW_WIDTH / 2 - 100 - body_font.size("Number of Turns")[0] / 2, 125,
                      (0, 0, 0))
        self.add_text("Score", WINDOW_WIDTH - 100 - body_font.size("S")[0], 125, (0, 0, 0))
        for i in range(len(plylist)):  # for loop to print the result for each player

            self.result(plylist, players, i, x)
            x += 75  # the difference between each result and result is 75
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


# Alex
class Game:
    def __init__(self):
        self.surface = guide_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.buttons = [
            ExitGameButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 44 * 39,
                           WINDOW_HEIGHT / 40 * 35,
                           (102, 17, 17),
                           (227, 190, 148), 'Exit'),
            DiceButton(self.surface, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 13, WINDOW_WIDTH / 5 * 4,
                       WINDOW_HEIGHT / 3 * 2 + 3,
                       (26, 107, 39),
                       (227, 190, 148), 'Roll the dice'),
        ]
        self.player_number = None
        self.players_names = []
        self.player_score = {}
        self.players_colors = {}
        self.players_order = Queue()
        self.dice_value = None
        self.dice_size = 80
        self.dice_surface = None
        self.dice_pos_x = None
        self.dice_pos_y = None

    def draw_score(self):
        for name in self.players_names:
            score = self.player_score[name]
            start_position = (WINDOW_WIDTH / 5 * 4, 0)
            k = 0
            for player in self.players_order:
                pygame.draw.rect(self.surface, self.players_colors[player][0],
                                 (start_position[0], start_position[1] + k, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 17))
                btn_txt = body_font.render(f'{player}:      {score}', True, "Black", None)
                r = btn_txt.get_rect()
                self.surface.blit(btn_txt,
                                  (start_position[0] + 10, start_position[1] + k + (WINDOW_HEIGHT / 17 - r.height) / 2))
                k += WINDOW_HEIGHT // 17
            turn_txt = NormalFont.render(f"{self.players_order.peek()}'s turn", True, "Black", None)
            cr = turn_txt.get_rect()
            self.surface.blit(turn_txt,
                              (WINDOW_WIDTH / 5 * 4 + (WINDOW_WIDTH / 5 - cr.width) / 2,
                               start_position[1] + k + (WINDOW_HEIGHT / 17 - cr.height) / 2))

    def draw_dice_screen(self):
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (WINDOW_WIDTH / 5 * 4, WINDOW_HEIGHT / 17 * 5, WINDOW_WIDTH / 5,
                          WINDOW_HEIGHT / 3 * 2 - WINDOW_HEIGHT / 7 * 2),
                         width=5)
        # if self.dice_value is not None:
        #     counter_txt = TitleFont.render(f"{self.dice_value}", True, "Black", None)
        #     r = counter_txt.get_rect()
        #     self.surface.blit(counter_txt, (WINDOW_WIDTH / 5 * 4 + (WINDOW_WIDTH / 5 - r.width) / 2,
        #                                     WINDOW_HEIGHT / 17 * 5 + (
        #                                                 WINDOW_HEIGHT / 3 * 2 - WINDOW_HEIGHT / 7 * 2 - r.height) / 2))
        if self.dice_surface is not None:
            self.surface.blit(self.dice_surface, (self.dice_pos_x, self.dice_pos_y))

    def draw_dice(self, value):
        self.dice_surface = pygame.Surface((self.dice_size, self.dice_size))
        self.dice_surface.fill((255, 255, 255))
        pygame.draw.rect(self.dice_surface, (0, 0, 0),
                         (0, 0, self.dice_size,
                          self.dice_size), width=4)
        if value in [1, 3, 5]:
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                             (self.dice_size / 2,
                              self.dice_size / 2), 6)
        if value in [2, 5, 4, 6]:
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                               (self.dice_size / 15 * 4,
                                self.dice_size / 15 * 11), 6)
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                               (self.dice_size / 15 * 11,
                                self.dice_size / 15 * 4), 6)
        if value in [5, 3, 4, 6]:
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                               (self.dice_size / 15 * 4,
                                self.dice_size / 15 * 4), 6)
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                               (self.dice_size / 15 * 11,
                                self.dice_size / 15 * 11), 6)
        if value == 6:
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                               (self.dice_size / 15 * 4,
                                self.dice_size / 2), 6)
            pygame.draw.circle(self.dice_surface, (0, 0, 0),
                               (self.dice_size / 15 * 11,
                                self.dice_size / 2), 6)
        self.surface.blit(self.dice_surface, (self.dice_pos_x, self.dice_pos_y))
        switch_screen(current_screen)
        pygame.display.flip()

    def dice_animation(self):
        for i in range(random.randrange(10, 20)):
            self.dice_pos_x = WINDOW_WIDTH / 5 * 4 + 10 + random.randrange(0, WINDOW_WIDTH // 5 - 20 - self.dice_size)
            self.dice_pos_y = WINDOW_HEIGHT / 17 * 5 + 10 + random.randrange(0, WINDOW_HEIGHT // 3 * 2 - WINDOW_HEIGHT // 7 * 2 - 20 - self.dice_size)
            self.draw_dice(random.randrange(1, 7))
            pygame.time.wait(150)
        self.draw_dice(self.dice_value)

    # This function draws everything, which will be on the screen
    def draw(self):
        self.surface.fill('white')
        for button in self.buttons:  # This draws each button on the screen
            button.draw()
        self.draw_score()
        self.draw_dice_screen()

    def roll_dice(self):
        self.dice_value = random.choice([1, 2, 3, 4, 5, 6])
        self.dice_animation()
        self.players_order.enqueue(self.players_order.dequeue())

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)

    def start_the_game(self):
        for name in self.players_names:
            self.player_score[name] = 0
        for name in list(set(self.players_names)):
            self.players_order.enqueue(name)
        for color, player in zip(random.sample(colors, self.player_number), self.players_names):
            self.players_colors[player] = color


class GameExit:
    def __init__(self):
        self.surface = guide_screen  # everything in menu class will be in the menu_screen surface
        # List of all buttons which will be in the menu
        # Each button initialized with its characteristics
        self.buttons = [
            ExitButton(self.surface, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 2 + 10,
                       WINDOW_HEIGHT / 2,
                       (102, 17, 17),
                       (227, 190, 148), 'Yes, exit!'),
            ReturnButton(self.surface, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 4,
                         WINDOW_HEIGHT / 2,
                         (26, 107, 39),
                         (227, 190, 148), 'Return to the game!'),
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
        self.surface.fill('white')
        small_page_txt = BigFont.render("Are you sure you want to exit the game?", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


#########################################################################################
#########################################################################################


class EnterField:
    def __init__(self, surf, width: float, height: float, pos_x: float, pos_y: float, text=''):
        self.surface = surf
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.activated = False

    # This function draw the button with the stated position
    def draw(self):
        if not self.activated:  # Drawing the button's shadow if the button isn't pressed
            pygame.draw.rect(self.surface, "gray", (self.pos_x, self.pos_y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, "white", (self.pos_x, self.pos_y, self.width, self.height))
        pygame.draw.rect(self.surface, "black", (self.pos_x, self.pos_y, self.width, self.height), width=2)
        btn_txt = NormalFont.render(self.text, True, 'black', None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, (self.pos_x + 5, self.pos_y + (self.height - r.height) / 2))

    # The function activates, when user click the mouse and check weather mouse was in the button at that moment
    def check(self, *args):
        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):
            # The function distinguish when user press the button and when they release the button
            # The function creates the animation (changes the position) of the button
            if args[0].type == 1025:
                self.activated = not self.activated
        elif self.activated and args[0].type == 1025:
            self.activated = not self.activated

    def inp(self, *args):
        if self.activated:
            if 97 <= args[0].key <= 122 or 48 <= args[0].key <= 57:
                if not self.text:
                    self.text += keys_codes[args[0].key].upper()
                elif len(self.text) <= 27:
                    self.text += keys_codes[args[0].key]
            elif args[0].key == 8:
                self.text = self.text[:-1]

    # This function is empty for the template
    # It is personalized for different buttons and reliable for button's jobd
    def do(self):
        pass


# Parental class for all buttons
class Button:
    # Initializing button with its position, color and text
    def __init__(self, surf, width: float, height: float, pos_x: float, pos_y: float, color_brick: tuple,
                 color_text=(255, 255, 255), text=''):
        self.surface = surf
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.btn_color = color_brick
        self.txt_color = color_text
        self.text = text
        self.pressed = False

    # This function draw the button with the stated position
    def draw(self):
        if not self.pressed:  # Drawing the button's shadow if the button isn't pressed
            pygame.draw.rect(self.surface, "black", (self.pos_x + 4, self.pos_y + 4, self.width, self.height))
        pygame.draw.rect(self.surface, self.btn_color, (self.pos_x, self.pos_y, self.width, self.height))
        self.add_txt()

    def add_txt(self):  # The function create a text of the button
        btn_txt = NormalFont.render(self.text, True, self.txt_color, None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, (self.pos_x + (self.width - r.width) / 2, self.pos_y + (self.height - r.height) / 2))

    # The function activates, when user click the mouse and check weather mouse was in the button at that moment
    def check(self, *args):
        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):
            # The function distinguish when user press the button and when they release the button
            # The function creates the animation (changes the position) of the button
            if args[0].type == 1025:
                self.pressed = True
                self.pos_x += 4
                self.pos_y += 4
            elif args[0].type == 1026:
                self.pressed = False
                self.pos_x -= 4
                self.pos_y -= 4
                self.do()
        if args[0].type == 1026 and self.pressed:
            self.pressed = False
            self.pos_x -= 4
            self.pos_y -= 4

    # This function is empty for the template
    # It is personalized for different buttons and reliable for button's job
    def do(self):
        pass


class StartButton(Button):  # Class for the button, which starts the game
    def add_txt(self):
        super().add_txt()
        self.draw_snake()  # This button has a unique design with a snake

    def draw_snake(self):  # This function draws the snake on the button
        if not self.pressed:  # Drawing the shadow of the snake
            pygame.draw.rect(self.surface, "black",
                             (self.pos_x - 20 + 4, self.pos_y + self.height - 8, 30, self.height + 85),
                             border_radius=20)
            pygame.draw.line(self.surface, "black",
                             (self.pos_x + self.width + 70 + 4, self.pos_y + self.height + 65 + 4),
                             (self.pos_x + self.width + 90 + 4, self.pos_y + self.height + 65 + 4), width=3)
            pygame.draw.rect(self.surface, "black",
                             (self.pos_x + self.width + 4, self.pos_y + self.height + 50 + 4, 70, 30),
                             border_radius=20)
        pygame.draw.rect(self.surface, (26, 107, 39), (self.pos_x - 20, self.pos_y - 25, 30, self.height + 200),
                         border_radius=20)
        pygame.draw.rect(self.surface, (26, 107, 39), (self.pos_x - 20, self.pos_y - 25, self.width + 50, 30),
                         border_radius=20)
        pygame.draw.rect(self.surface, (26, 107, 39), (self.pos_x + self.width, self.pos_y - 25, 30, self.height + 100),
                         border_radius=20)
        pygame.draw.line(self.surface, "red", (self.pos_x + self.width + 70, self.pos_y + self.height + 65),
                         (self.pos_x + self.width + 90, self.pos_y + self.height + 65), width=3)
        pygame.draw.rect(self.surface, (26, 107, 39), (self.pos_x + self.width, self.pos_y + self.height + 50, 70, 30),
                         border_radius=20)
        pygame.draw.circle(self.surface, "black", (self.pos_x + self.width + 60, self.pos_y + self.height + 59),
                           radius=2)
        pygame.draw.circle(self.surface, "black", (self.pos_x + self.width + 60, self.pos_y + self.height + 71),
                           radius=2)

    def do(self):  # This button opens number of players choice window
        global current_screen
        choice.player_number = 1
        current_screen = choice


class BoardButton(Button):  # Class for the button which opens window of leaderboard
    def do(self):
        global current_screen
        current_screen = board


class GuideButton(Button):  # Class for the button which opens window with player guide
    def do(self):
        print("Let's learn how to play")
        global current_screen
        current_screen = guide


class ArrowUpButton(Button):
    def draw(self):
        if not self.pressed:
            pygame.draw.polygon(self.surface, 'black', [(self.pos_x + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width / 2 + 4,
                                                         self.pos_y - self.height + 4)])
        pygame.draw.polygon(self.surface, self.btn_color, [(self.pos_x, self.pos_y),
                                                           (self.pos_x + self.width, self.pos_y),
                                                           (self.pos_x + self.width / 2, self.pos_y - self.height)])

    def check(self, *args):
        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y - self.height <= p[1] <= self.pos_y):
            if args[0].type == 1025:
                self.pressed = True
                self.pos_x += 4
                self.pos_y += 4
            elif args[0].type == 1026:
                self.pressed = False
                self.pos_x -= 4
                self.pos_y -= 4
                self.do()
        if args[0].type == 1026 and self.pressed:
            self.pressed = False
            self.pos_x -= 4
            self.pos_y -= 4

    def do(self):
        choice.player_number = choice.player_number % 4 + 1


class ArrowDownButton(Button):
    def draw(self):
        if not self.pressed:
            pygame.draw.polygon(self.surface, 'black', [(self.pos_x + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width / 2 + 4,
                                                         self.pos_y + self.height + 4)])
        pygame.draw.polygon(self.surface, self.btn_color, [(self.pos_x, self.pos_y),
                                                           (self.pos_x + self.width, self.pos_y),
                                                           (self.pos_x + self.width / 2, self.pos_y + self.height)])

    def check(self, *args):
        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):
            if args[0].type == 1025:
                self.pressed = True
                self.pos_x += 4
                self.pos_y += 4
            elif args[0].type == 1026:
                self.pressed = False
                self.pos_x -= 4
                self.pos_y -= 4
                self.do()
        if args[0].type == 1026 and self.pressed:
            self.pressed = False
            self.pos_x -= 4
            self.pos_y -= 4

    def do(self):
        choice.player_number = choice.player_number - 1
        if choice.player_number == 0:
            choice.player_number = 4


class ExitButton(Button):  # Class for the button which return the user to the menu
    def do(self):
        global current_screen
        current_screen = menu


class ExitAppButton(Button):  # Class for the button which stops the app
    def do(self):
        global running
        running = False


class ExitGameButton(Button):  # Class for the button which stops the app
    def do(self):
        global current_screen
        current_screen = gexit


class ReturnButton(Button):  # Class for the button which return the user to the menu
    def do(self):
        global current_screen
        current_screen = game


class ChoiceSubmitButton(Button):
    def do(self):
        global current_screen, names
        names = Names()
        current_screen = names


class NamesSubmitButton(Button):
    def do(self):
        global current_screen, game
        game = Game()
        for field in names.fields:
            game.players_names.append(field.text)
        if len(set(game.players_names)) == len(game.players_names):
            game.player_number = choice.player_number
            current_screen = game
            game.start_the_game()
        else:
            names.same_name_error = True


class DiceButton(Button):
    def do(self):
        global current_screen, game
        game.roll_dice()


# "Switch screen" function which triggers at the end of each pygame loop and displays current surface
def switch_screen(screen):
    screen.draw()
    main_screen.blit(screen.surface, (0, 0))


menu = Menu()
guide = Guide()
board = Leaderboard()
choice = Choice()
names = Names()
game = Game()
gexit = GameExit()
current_screen = menu
while running:  # Window cycle
    for event in pygame.event.get():  # Event check
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            current_screen.check(event)
        if event.type == pygame.KEYDOWN and current_screen == names:
            current_screen.inp(event)
    switch_screen(current_screen)
    pygame.display.flip()
    clock.tick(FPS)  # Setting the amount of frames per seconds (limits of updates per second)
pygame.quit()
