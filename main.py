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
# Dictionary to encode users keyboard input
keys_codes = {48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 97: 'a',
              98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k',
              108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
              118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}
# Colors available for players - each contains value for circle and a softer one for score board
colors = [[(237, 152, 152), (222, 35, 35)], [(189, 152, 237), (116, 35, 222)], [(152, 170, 237), (35, 76, 222)],
          [(152, 237, 237), (35, 222, 222)], [(152, 237, 196), (35, 222, 132)],
          [(169, 237, 152), (73, 222, 35)], [(220, 237, 152), (185, 222, 35)],
          [(237, 229, 152), (222, 203, 35)], [(237, 203, 152), (222, 147, 35)],
          [(237, 187, 152), (222, 113, 35)], [(237, 162, 152), (222, 57, 35)]]

# Game board size settings constants
CELL_SIZE = 120
ROWS = 5
COLS = 8
# Fonts
BigFont = pygame.font.SysFont("Arial", 60)
NormalFont = pygame.font.SysFont("Arial", 32)
TitleFont = pygame.font.SysFont("Arial", 100)
BodyFont = pygame.font.SysFont("Arial", 25)
# Creating a file with logs for debugging and error-handling
log_file_name = 'game_log.txt'
with open(log_file_name, 'w') as file:
    print('\t\t\t______LOGS OF THE CURRENT GAME______\n\n', file=file)

######################## Omar
# Storing player's data
players = {
    "Omar": [3, 20],
    "Alex": [10, 80],
    "Wilson": [2, 0]
}

######################## Alex
# Creating different surfaces for different purpose
# One general and one for each window
main_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
menu_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
guide_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
leader_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
choice_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
names_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_exit_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_end_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Merge sort algorithm for players dictionary block
def merge(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i][2] > right[j][2]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged += left[i:]
    merged += right[j:]
    return merged


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    return merge(left_sorted, right_sorted)


def dict_list(di: dict) -> list:
    li = []
    for i in di:
        li.append((i, di[i][0], di[i][1]))
    return li


def list_dict(li: list) -> dict:
    di = {}
    for i in li:
        di[i[0]] = [i[1], i[2]]
    return di


def dict_merge_sort(di: dict) -> dict:
    try:  # Error handling if for some reason(later we make it impossible) exception occurred
        result = list_dict(merge_sort(dict_list(di)))
        return result
    except Exception as exception:
        with open(log_file_name, 'a') as log_file:
            print(f'\n!!!!ERROR!!! {type(exception).__name__} occurred', file=log_file)


# Queue to manage players' order during the game
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

    def __str__(self):  # This function was created for debugging to correctly display the queue
        return ', '.join(list(map(str, self.items)))

    def size(self):
        return len(self.items)

    def __iter__(self):  # Iterator for the Queue to run across the Queue
        self.ln = self.size()
        return self

    def __next__(self):  # Part of iterator
        if self.ln <= 0:
            raise StopIteration
        self.ln -= 1
        return self.items[self.ln]


######################## Omar
# class cell
class Cell:
    def __init__(self, row, col, val, index):
        self.row = row
        self.col = col
        self.val = val
        self.index = index
        self.connections = []

    # function to add a neighbor inside the connection list
    def add_connection(self, neighbor):
        self.connections.append(neighbor)

    def __str__(self):
        return f"{self.row}, {self.col}, {self.index}, {self.val}"


######################## Alex
#########################################################################################
##################################   WINDOWS CLASSES BLOCK   ##########################################
# Each window is described as a class, which draws everything, that must be drawn
# and helps to connect user and every interactive piece of the window

# Class for the menu
class Menu:
    """
    Fills menu screen with content, so it can be displayed in the main cycle
        Menu screen gives user ability to choose to which next window they want to proceed

        Stores information about elements of menu screen:
            --Surface - to draw on
            --Buttons - which should be drawn in the surface

        Process each signals from user, when they interact with menu screen
    """

    def __init__(self):
        """Initialise window and states all essential properties"""
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

    def draw(self):
        """Draws buttons and text"""
        self.surface.fill('white')
        btn_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):
        """Executes every user request"""
        for button in self.buttons:
            button.check(user_event)


# Class for the window where user can choose amount of players
class Choice:
    """
    Fills choice screen with content, so it can be displayed in the main cycle
        Choice screen gives user ability to choose amount of players for the game

        Stores information about elements of choice screen:
            --Surface - to draw on
            --Number of players - stores current chosen amount of players
            --Buttons - which should be drawn in the surface

        Process each signals from user, when they interact with choice screen
    """

    def __init__(self):
        """Initialise window and states all essential properties"""
        self.surface = choice_screen  # everything in choice class will be in the choice_screen surface
        # List of all buttons which will be in the screen
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

    def draw(self):
        """Draws buttons and text"""
        self.surface.fill('white')
        page_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render("Choose amount of players", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))

        # Display the current chosen amount of players
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (WINDOW_WIDTH / 7 * 3, WINDOW_HEIGHT / 7 * 3, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7 * 2),
                         width=5)
        counter_txt = TitleFont.render(f"{self.player_number}", True, "Black", None)
        r = counter_txt.get_rect()
        self.surface.blit(counter_txt, (WINDOW_WIDTH / 7 * 3 + (WINDOW_WIDTH / 7 - r.width) / 2,
                                        WINDOW_HEIGHT / 7 * 3 + (WINDOW_HEIGHT / 7 * 2 - r.height) / 2))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):
        """Executes every user request"""
        for button in self.buttons:
            button.check(user_event)


class Names:
    """
    Fills names screen with content, so it can be displayed in the main cycle
        Names screen gives user ability to enter names of players

        Stores information about elements of names screen:
            --Surface - to draw on
            --Buttons - stores buttons which should be drawn in the surface
            --Fields - stores names enter fields which should be drawn in the surface
                depend on the previously chosen amount of players
            --Names error - error handling system, which doesn't let user enter same names in the fields

        Process each signals from user, when they interact with names screen
    """

    def __init__(self):
        """Initialise window and states all essential properties"""
        self.surface = names_screen  # everything in names class will be in the names_screen surface
        # List of all buttons which will be in the screen
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
        # List of all input fields which will be in the menu
        # Each input field initialized with its characteristics
        self.fields = []
        for i in range(choice.player_number):
            self.fields.append(EnterField(self.surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 4,
                                          WINDOW_HEIGHT / 5 * 2 + WINDOW_HEIGHT / 9 * i))
        self.same_name_error = False  # User won't be able to proceed to the game if value is True

    def draw(self):
        """Draws buttons, type fields  and text"""
        self.surface.fill('white')
        page_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render("Enter name(s) of player(s)", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        if self.same_name_error:  # Program checks weather all names are different
            warning_txt = NormalFont.render("All names must be different", True, "Red", None)
            r = warning_txt.get_rect()
            self.surface.blit(warning_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 3 + 5))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()
        for field in self.fields:  # This draws each input field on the screen
            field.draw()

    def check(self, user_event):
        """Executes every user request"""
        for button in self.buttons:
            button.check(user_event)
        for field in self.fields:
            field.check(user_event)

    def inp(self, user_event):
        """Execute every user request from the keyboard"""
        for field in self.fields:
            field.inp(user_event)


# This function would've worked if we had been able to make our game as .exe file or as zip archive
# The idea was to upload word file of guide into this window
class Guide:
    def __init__(self):
        self.surface = guide_screen  # everything in guide class will be in the guide_screen surface
        # List of all buttons which will be in the quide
        # Each button initialized with its characteristics
        self.buttons = [
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


######################## Omar
class Leaderboard:
    """
    Fills leader board screen with content, so it can be displayed in the main cycle
        Leader board screen gives user ability to see previous result of players

        Stores information about elements of leader board screen:
            --Surface - to draw on
            --Buttons - stores buttons which should be drawn in the surface
            --Body Height - helps calculate height of boxes for the scores

        Process each signals from user, when they interact with leader board screen
    """

    def __init__(self):
        """Initialises window and states all essential properties"""
        self.surface = leader_screen
        self.buttons = [
            ExitButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 44 * 39,
                       WINDOW_HEIGHT / 40 * 35,
                       (102, 17, 17),
                       (227, 190, 148), 'Exit'),
        ]
        self.bodyheight = BodyFont.size("Body")[1]

    def add_text(self, txt, wid, hig, color=(227, 190, 148)):
        """Adds text in the stated positions in the surface"""
        body_surface = BodyFont.render(str(txt), True, color)
        self.surface.blit(body_surface, (wid, hig))

    def result(self, li, di, i, y):
        """Draws a line for one player"""
        pygame.draw.line(self.surface, (102, 61, 14), (0, y), (WINDOW_WIDTH, y), 50)
        self.add_text(str(i + 1), 0, y + self.bodyheight / 2 - 25)
        self.add_text(str(li[i]), WINDOW_WIDTH / 4 - 100, y + self.bodyheight // 2 - 25)
        self.add_text(str(di[li[i]][0]), WINDOW_WIDTH / 2 - 100, y + self.bodyheight / 2 - 25)
        self.add_text(str(di[li[i]][1]), WINDOW_WIDTH - 100, y + self.bodyheight / 2 - 25)

    def draw(self):
        """Draws everything"""
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
        self.add_text("Number of Turns", WINDOW_WIDTH / 2 - 100 - BodyFont.size("Number of Turns")[0] / 2, 125,
                      (0, 0, 0))
        self.add_text("Score", WINDOW_WIDTH - 100 - BodyFont.size("S")[0], 125, (0, 0, 0))
        plylist = list(players.keys())
        for i in range(len(plylist)):  # for loop to print the result for each player
            if i > 5:  # maximum 6 players at one time
                break
            self.result(plylist, players, i, x)
            x += 75  # the difference between each result and result is 75
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):
        """Execute every user request"""
        for button in self.buttons:
            button.check(user_event)


######################## Alex
class Game:
    """
    Fills game screen with content, so it can be displayed in the main cycle
        Game screen is the game itself

        Stores information about elements of leader board screen:
            --Surface - to draw on
            --Buttons - stores buttons which should be drawn in the surface
            --Number of players - this value is taken from the Choice class
            --Players' names - list of values taken from the Names class
            --Players' score - dynamic dictionary which stores players scores during the game
                When the game starts each player's score set to 0 by default
            --Players' colors - stores colores, linked to the players
                When the game starts each player is randomly linked with color from prepared list 'colors'
            --Players' order - is a queue which helps track order of players
                When the game starts it is filled with their names
            --Dice Value - stores current value from 1 to 6, randomly picked when user hits button 'Roll the die'
            --Dice size - just constant, created to easily test interface and appearance without changing code a lot
            --Dice surface - dice have their own surface to be drawn in
                This solution makes dice animation code more readable
            --Dice position - two variables which store final dice position after a roll
            --Turns - this variable counts die rolls
            --Game board - stores attribute of class 'Board' - game board with ladders and snakes
                Initialized when the game is started
            --Players positions - stores cell in which players stays during the game
                When the game is started it is filled with players' names and sets their positions to the beginning
            --Finished - flag which states that the game is on, used when the game is finished to not update the queue

        Process each signals from user, when they interact with leader board screen
    """

    def __init__(self):
        """Initialises window and states all essential properties"""
        self.surface = game_screen
        self.buttons = [
            ExitGameButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 44 * 39,
                           WINDOW_HEIGHT / 40 * 35,
                           (102, 17, 17),
                           (227, 190, 148), 'Exit'),
            DiceButton(self.surface, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 13, WINDOW_WIDTH / 5 * 4,
                       WINDOW_HEIGHT / 3 * 2 + 3,
                       (26, 107, 39),
                       (227, 190, 148), 'Roll the die'),
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
        self.turns = 0
        self.game_board = None
        self.players_positions = {}
        self.finished = False

    def end_game(self):
        """
        Function which will do all necessary actions, when someone reach the end of the board

            When the game is over:
                Raise the flag of finish
                Updates global dictionary, which stores players' scores for the leader board
                Changes the screen to the result screen
        """
        global current_screen, players
        self.finished = True
        for name in self.player_score:
            if name not in players:
                players[name] = [self.turns // len(self.players_names) + 1, self.player_score[name]]
            else:
                players[name][0] += self.turns // len(self.players_names) + 1
                players[name][1] += self.player_score[name]
        players[self.players_order.peek()][1] += 50  # The winner takes 50 extra points
        current_screen = endgame

    def draw_score(self):
        """Function to draw and update current score information in the top right corner"""
        start_position = (WINDOW_WIDTH / 5 * 4, 0)
        k = 0
        # Queue is iterable so program can draw the scoreboard according to their current order
        for player in self.players_order:
            score = self.player_score[player]
            pygame.draw.rect(self.surface, self.players_colors[player][0],
                             (start_position[0], start_position[1] + k, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 17))
            btn_txt = BodyFont.render(f'{player}:      {score}', True, "Black", None)
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
        """Function creates space for dice roll"""
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (WINDOW_WIDTH / 5 * 4, WINDOW_HEIGHT / 17 * 5, WINDOW_WIDTH / 5,
                          WINDOW_HEIGHT / 3 * 2 - WINDOW_HEIGHT / 7 * 2),
                         width=5)

        # The following part was used for debugging, before implementing dice animation

        # if self.dice_value is not None:
        #     counter_txt = TitleFont.render(f"{self.dice_value}", True, "Black", None)
        #     r = counter_txt.get_rect()
        #     self.surface.blit(counter_txt, (WINDOW_WIDTH / 5 * 4 + (WINDOW_WIDTH / 5 - r.width) / 2,
        #                                     WINDOW_HEIGHT / 17 * 5 + (
        #                                                 WINDOW_HEIGHT / 3 * 2 -
        #                                                 WINDOW_HEIGHT / 7 * 2 - r.height) / 2))

        if self.dice_surface is not None:
            self.surface.blit(self.dice_surface, (self.dice_pos_x, self.dice_pos_y))

    def draw_dice(self, value):
        """Function draw certain picture of dice depend on its result"""
        self.dice_surface = pygame.Surface((self.dice_size, self.dice_size))
        self.dice_surface.fill((255, 255, 255))
        pygame.draw.rect(self.dice_surface, (0, 0, 0),
                         (0, 0, self.dice_size,
                          self.dice_size), width=4)
        # All die sides have something in common - there is no need to create 6 different if statements
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
        switch_screen(current_screen)
        pygame.display.flip()  # Extra flip is essential to show animation correctly

    def dice_animation(self):
        """Function creates dice animation, when pressed dice roll button"""
        for i in range(random.randrange(10, 20)):  # The amount of frames for animation is randomly picked
            self.dice_pos_x = WINDOW_WIDTH / 5 * 4 + 10 + random.randrange(0, WINDOW_WIDTH // 5 - 20 - self.dice_size)
            self.dice_pos_y = WINDOW_HEIGHT / 17 * 5 + 10 + random.randrange(0,
                                                                             WINDOW_HEIGHT // 3 * 2 - WINDOW_HEIGHT //
                                                                             7 * 2 - 20 - self.dice_size)
            self.draw_dice(random.randrange(1, 7))
            pygame.time.wait(150)  # The function freezes the program for a bit so the animation can be noticed
        self.draw_dice(self.dice_value)

    def draw_players(self):
        """Function draws circles of different colors which depict players and their positions in the board"""
        k_x = CELL_SIZE / 4
        k_y = CELL_SIZE / 4
        c = 0
        for player in self.players_names:
            h_x = 20 + self.players_positions[player][1] * CELL_SIZE + k_x
            h_y = 40 + self.players_positions[player][0] * CELL_SIZE + k_y
            pygame.draw.circle(self.surface, self.players_colors[player][1], (h_x, h_y), CELL_SIZE / 8)
            if c % 2 == 0:
                k_x += CELL_SIZE / 2
                k_x %= CELL_SIZE
            else:
                k_y += CELL_SIZE / 2
                k_x %= CELL_SIZE
            c += 1

    def move(self):
        """Function move the player's circles when player roll a die"""
        player = self.players_order.peek()
        h_x = self.players_positions[player][1]
        h_y = self.players_positions[player][0]
        if h_y == 0 and h_x + self.dice_value >= COLS:  # When program cannot move player anywhere the game stops
            self.end_game()
        else:
            if h_x + self.dice_value < COLS and h_y % 2 == 0:
                self.players_positions[player][1] += self.dice_value
            elif h_x - self.dice_value >= 0 and h_y % 2 == 1:
                self.players_positions[player][1] -= self.dice_value
            elif h_y % 2 == 0:
                self.players_positions[player][0] -= 1
                self.players_positions[player][1] = COLS - (self.dice_value - (COLS - h_x)) - 1
            elif h_y % 2 == 1:
                self.players_positions[player][0] -= 1
                self.players_positions[player][1] = self.dice_value - h_x - 1
            connected = self.game_board.cells[self.players_positions[player][0]][
                self.players_positions[player][1]].connections
            if connected:
                if connected[0] is not None:  # Check if the cell is connected with another cell with ladder or snake
                    self.players_positions[player][0] = connected[0].row
                    self.players_positions[player][1] = connected[0].col
            self.player_score[player] += self.game_board.cells[self.players_positions[player][0]][
                self.players_positions[player][1]].val  # Updates player's score after their turn

    def draw(self):
        """This function draws and blits everything, calls all drawing methods, which will be on the screen"""
        self.surface.fill('white')
        self.game_board.draw_board()
        for button in self.buttons:  # This draws each button on the screen
            button.draw()
        self.draw_score()
        self.draw_dice_screen()
        self.surface.blit(self.game_board.surface, (20, 40))  # Draws board
        self.draw_players()

    def roll_dice(self):
        """This function is called, when player hits button 'Roll The die' and triggers all connected methods"""
        self.dice_value = random.choice([1, 2, 3, 4, 5, 6])  # States final die result

        # self.dice_value = random.choice([1])   Was used during debugging to handle randomness and debug movements

        self.dice_animation()
        self.turns += 1
        self.move()
        with open(log_file_name, 'a') as log_file:
            print(f'Turn {self.turns}; Player: {self.players_order.peek()}; Die rolled: {self.dice_value}; '
                  f'New player position: {self.players_positions[self.players_order.peek()]}', file=log_file)
        if not self.finished:  # Stops players' rotation when the game is over
            self.players_order.enqueue(self.players_order.dequeue())

    def check(self, user_event):
        """Execute every user request"""
        for button in self.buttons:
            button.check(user_event)

    def start_the_game(self):
        """Function states important values to start the game"""
        self.game_board = Board()  # Initialize and create game board
        self.game_board.cells[ROWS - 1][0].val = 0
        for name in self.players_names:  # Brings inputted players' names into the game
            self.player_score[name] = 0
        for name in list(set(self.players_names)):  # Creates queue for players' order
            self.players_order.enqueue(name)
        # Links player and color
        for color, player in zip(random.sample(colors, self.player_number), self.players_names):
            self.players_colors[player] = color
        for player in self.players_names:  # States starting position for all players
            self.players_positions[player] = [ROWS - 1, 0]  # Left bottom cell is the beginning


######################## Omar
class Board:
    """
    Creates and draw a board for the game:

        Stores information about elements of the board screen:
            --Rows - amount of rows in the board - taken from constant and can be easily changed for debugging
            --Columns - amount of columns in the board - taken from constant and can be easily changed for debugging
            --Surface - to draw on
            --Cells - graph with row*columns nodes which contains cells of the board

        Creates ladder-and-snake connections between cells
    """

    def __init__(self):
        """Initialises window and states all essential properties"""
        self.rows = ROWS
        self.cols = COLS
        self.surface = pygame.Surface((self.cols * CELL_SIZE, self.rows * CELL_SIZE))
        self.cells = [[] for row in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if row % 2 == 0:
                    index = (self.rows - row) * self.cols - self.cols + 1 + col
                else:
                    index = (self.rows - row) * self.cols - col
                #  Randomly generates a value for the cell between -35 and 50
                self.cells[row].append(Cell(row, col, random.randrange(-35, 50), index))
        self.create_ladders()
        self.create_snakes()

    def create_ladders(self):
        """Connects two cells by a brown line - ladder - as a shortcut"""
        k = 0
        while k < 2:  # In the board cannot be less than 2 ladders
            # The amount of ladders is random - between 2 and 6(which is quite unlikely)
            for i in range(random.randrange(3, 5)):
                # Cells to connect are picked randomly
                a_row = random.randint(0, self.rows - 1)
                a_col = random.randint(0, self.cols - 1)
                b_row = random.randint(0, a_row)
                b_col = random.randint(0, self.cols - 1)
                if a_row != b_row and not self.cells[a_row][a_col].connections and not \
                        self.cells[b_row][b_col].connections:  # so there is no ladders in the same row
                    self.cells[a_row][a_col].add_connection(self.cells[b_row][b_col])
                    # Program will know, that cell has a connection
                    # but as far as the graph is orientated this connection won't be considered
                    self.cells[b_row][b_col].add_connection(None)
                    k += 1

    # it will connect two cells by a green line as a shortcut
    def create_snakes(self):
        """Connects two cells by a green line - snake - as a shortcut"""
        t = 0
        while t < 2:  # In the board cannot be less than 2 snakes
            # The amount of snakes is random - between 2 and 6(which is quite unlikely)
            for i in range(random.randrange(3, 5)):
                # Cells to connect are picked randomly
                a_row = random.randint(0, self.rows - 1)
                a_col = random.randint(0, self.cols - 1)
                b_row = random.randint(a_row, self.rows - 1)
                b_col = random.randint(0, self.cols - 1)
                if a_row != b_row and not self.cells[a_row][a_col].connections and not \
                        self.cells[b_row][b_col].connections:  # so there is no snakes in the same row
                    self.cells[a_row][a_col].add_connection(self.cells[b_row][b_col])
                    # Program will know, that cell has a connection
                    # but as far as the graph is orientated this connection won't be considered
                    self.cells[b_row][b_col].add_connection(None)
                    t += 1

    #
    def draw_board(self):
        """Draws the board with a size stated in the constant for each cell and the order of cells on the board"""
        # Cells must be on the foreground
        self.surface.fill((200, 200, 200))
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    color = (139, 189, 120)
                else:
                    color = (200, 200, 200)
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.surface, color, rect)
        # Ladders and snakes must be above cells, but under in-cell information
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].connections:
                    if self.cells[row][col].connections[0] is not None:
                        if self.cells[row][col].index < self.cells[row][col].connections[0].index:
                            line_color = (102, 61, 14)
                        else:
                            line_color = (26, 107, 39)
                        b_row = self.cells[row][col].connections[0].row
                        b_col = self.cells[row][col].connections[0].col
                        x1, y1 = self.cells[row][col].col * CELL_SIZE + CELL_SIZE / 2, self.cells[row][
                            col].row * CELL_SIZE + CELL_SIZE / 2
                        x2, y2 = self.cells[b_row][b_col].col * CELL_SIZE + CELL_SIZE / 2, self.cells[b_row][
                            b_col].row * CELL_SIZE + CELL_SIZE / 2
                        pygame.draw.line(self.surface, line_color, (x1, y1), (x2, y2), 15)
        # Add information about number of the cell and points inside
        for row in range(0, self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                x_font = pygame.font.SysFont("Arial", 25)
                y_font = pygame.font.SysFont("Comic Sans MS", 20)
                text_index = y_font.render(str(self.cells[row][col].index), True, (0, 0, 0))
                text_surface = x_font.render(str(self.cells[row][col].val), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                index_rect = list(text_index.get_rect(bottomright=rect.bottomright))
                self.surface.blit(text_surface, text_rect)
                self.surface.blit(text_index, (index_rect[0], index_rect[1]))


######################## Alex
# Class used when user try to exit during the game
class GameExit:
    """
    Fills game exit screen with content, so it can be displayed in the main cycle
        Game exit screen appears, when user tries to exit the game while playing
            and asks if user truly wants to exit the game or suggest to return

        Stores information about elements of game exit screen:
            --Surface - to draw on
            --Buttons - stores buttons which should be drawn in the surface

        Process each signals from user, when they interact with game exit screen
    """
    def __init__(self):
        """Initialises window and states all essential properties"""
        self.surface = game_exit_screen
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

    def draw(self):
        """This function draws everything, which will be on the screen"""
        self.surface.fill('white')
        small_page_txt = BigFont.render("Are you sure you want to exit the game?", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):
        """Execute every user request"""
        for button in self.buttons:
            button.check(user_event)


class GameEnd:
    """
    Fills game result screen with content, so it can be displayed in the main cycle
        Game result screen appears, when the game is over and show results of the game

        Stores information about elements of game result screen:
            --Surface - to draw on
            --Buttons - stores buttons which should be drawn in the surface

        Process each signals from user, when they interact with game result screen
    """
    def __init__(self):
        """Initialises window and states all essential properties"""
        self.surface = game_end_screen
        self.buttons = [
            ExitButton(self.surface, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 2 + 10,
                       WINDOW_HEIGHT / 2,
                       (102, 17, 17),
                       (227, 190, 148), 'Return to the menu'),
            StartButton(self.surface, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 4,
                        WINDOW_HEIGHT / 2,
                        (26, 107, 39),
                        (227, 190, 148), 'Start a new game'),
        ]

    def draw(self):
        """This function draws everything, which will be on the screen"""
        self.surface.fill('white')
        page_txt = TitleFont.render("The game is over", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render(
            f"The winner is {game.players_order.peek()} with score "
            f"{game.player_score[game.players_order.peek()]} points",
            True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):
        """Execute every user request"""
        for button in self.buttons:
            button.check(user_event)


#########################################################################################
###############################    INTERACTIVE PARTS    #########################################


# Class which imitates input box
class EnterField:
    """
    Class, which describes field to input text for the keyboard
        Activates/disactivates when clicked by user
        Allows to enter maximum 27 common characters - latin letters and numbers

        Stores information about the field:
            --Surface - to draw on
            --Size
            --Position
            --Text - characters, which user has inputted in the field
            --Activated - to verify, that the field has been activated and can be edited

        Process each signals from user, when they interact with current screen
    """
    def __init__(self, surf, width: float, height: float, pos_x: float, pos_y: float, text=''):
        """Initialises field and states all essential properties"""
        self.surface = surf
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.activated = False

    def draw(self):
        """Draws the field"""
        # Depend on was the field activated or not it has different color
        if not self.activated:
            pygame.draw.rect(self.surface, "gray", (self.pos_x, self.pos_y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, "white", (self.pos_x, self.pos_y, self.width, self.height))
        pygame.draw.rect(self.surface, "black", (self.pos_x, self.pos_y, self.width, self.height), width=2)
        btn_txt = NormalFont.render(self.text, True, 'black', None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, (self.pos_x + 5, self.pos_y + (self.height - r.height) / 2))

    def check(self, *args):
        """Function activates or disactivates field when it's pressed by user"""
        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):
            if args[0].type == 1025:
                self.activated = not self.activated
        elif self.activated and args[0].type == 1025:
            self.activated = not self.activated

    def inp(self, *args):
        """Add characters, when get any signals from the keyboard"""
        if self.activated:
            if 97 <= args[0].key <= 122 or 48 <= args[0].key <= 57:
                if not self.text:
                    self.text += keys_codes[args[0].key].upper()
                elif len(self.text) <= 27:
                    self.text += keys_codes[args[0].key]
            elif args[0].key == 8:  # Text can be deleted with 'Delete' button in the keyboard
                self.text = self.text[:-1]


# Parental class for all buttons
class Button:
    """
    Class, which describes common button and this class is a parental class for all buttons
        When user clicks mouse checks if they clicked inside button area
        If click was for the button triggers function 'do' which contains button action
        Handle situation when the button is clicked but while it's clicked mouse is moved away from the button

        Stores information about the field:
            --Surface - to draw on
            --Size
            --Position
            --Color of the button
            --Color of the button's text
            --Text for the button - by default is empty string
            --Pressed - to verify, that the button is pressed at the moment if it is -
                button's animation will be changed

        Process each signals from user, when they interact with current screen
    """

    def __init__(self, surf, width: float, height: float, pos_x: float, pos_y: float, color_brick: tuple,
                 color_text=(255, 255, 255), text=''):
        """Initialises field and states all essential properties"""
        self.surface = surf
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.btn_color = color_brick
        self.txt_color = color_text
        self.text = text
        self.pressed = False

    def draw(self):
        """This function draw the button with the stated position"""
        if not self.pressed:  # Drawing the button's shadow if the button isn't pressed
            pygame.draw.rect(self.surface, "black", (self.pos_x + 4, self.pos_y + 4, self.width, self.height))
        pygame.draw.rect(self.surface, self.btn_color, (self.pos_x, self.pos_y, self.width, self.height))
        self.add_txt()

    def add_txt(self):
        """The function create a text of the button"""
        btn_txt = NormalFont.render(self.text, True, self.txt_color, None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, (self.pos_x + (self.width - r.width) / 2, self.pos_y + (self.height - r.height) / 2))

    def check(self, *args):
        """Activates, when user click the mouse and check weather mouse was in the button's area at that moment"""
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
        if args[0].type == 1026 and self.pressed:  # Handling the problem with the mouse, which was moved away
            self.pressed = False
            self.pos_x -= 4
            self.pos_y -= 4
            with open(log_file_name, 'a') as log_file:
                print(f'\nError user tried to move mouse from button {type(self)} is handled', file=log_file)

    def do(self):
        """
        This function is empty for the template
            It is personalized for different buttons and reliable for button's job
        """
        pass


class StartButton(Button):  # Class for the button, which starts the game
    """
    Button which starts the game
        Inherit from the 'Button' class
        Draw for the button addition design detail - snake
    """
    def add_txt(self):
        super().add_txt()
        self.draw_snake()  # This button has a unique design with a snake

    def draw_snake(self):
        """This function draws the snake on the button"""
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

    def do(self):
        """Changes current screen to the choice window"""
        global current_screen
        choice.player_number = 1  # By default, number of players is 1
        current_screen = choice


class BoardButton(Button):
    """
    Button which opens leader board
        Inherit from the 'Button' class
    """
    def do(self):
        """Changes current screen to the board window"""
        global current_screen, players
        players = dict_merge_sort(players)
        current_screen = board


class GuideButton(Button):
    """
    Button which opens guide
        Inherit from the 'Button' class
    """
    def do(self):
        """Changes current screen to the guide window"""
        print("Let's learn how to play")
        global current_screen
        current_screen = guide


class ArrowUpButton(Button):
    """
    Button which rises amount of players, when user choose it in the choice screen
        Inherit from the 'Button' class
    """
    def draw(self):
        """This function draw triangle button with the stated position"""
        if not self.pressed:
            pygame.draw.polygon(self.surface, 'black', [(self.pos_x + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width / 2 + 4,
                                                         self.pos_y - self.height + 4)])
        pygame.draw.polygon(self.surface, self.btn_color, [(self.pos_x, self.pos_y),
                                                           (self.pos_x + self.width, self.pos_y),
                                                           (self.pos_x + self.width / 2, self.pos_y - self.height)])

    def check(self, *args):
        """Activates, when user click the mouse and check weather mouse was in the button's area at that moment"""
        # Because of the another form of the button the checking function was changed
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
        """Changes the chosen amount of players"""
        choice.player_number = choice.player_number % 4 + 1


class ArrowDownButton(Button):
    """
    Button which decrease amount of players, when user choose it in the choice screen
        Inherit from the 'Button' class
    """
    def draw(self):
        """This function draw triangle button with the stated position"""
        if not self.pressed:
            pygame.draw.polygon(self.surface, 'black', [(self.pos_x + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width / 2 + 4,
                                                         self.pos_y + self.height + 4)])
        pygame.draw.polygon(self.surface, self.btn_color, [(self.pos_x, self.pos_y),
                                                           (self.pos_x + self.width, self.pos_y),
                                                           (self.pos_x + self.width / 2, self.pos_y + self.height)])

    def check(self, *args):
        """Activates, when user click the mouse and check weather mouse was in the button's area at that moment"""
        # Because of the another form of the button the checking function was changed
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
        """Changes the chosen amount of players"""
        choice.player_number = choice.player_number - 1
        if choice.player_number == 0:
            choice.player_number = 4


class ExitButton(Button):
    """
    Button which returns user to the menu screen
        Inherit from the 'Button' class
    """
    def do(self):
        """Changes current screen to the menu window"""
        global current_screen
        current_screen = menu


class ExitAppButton(Button):
    """
    Button which allows to exit the application and stop running it
        Inherit from the 'Button' class
    """
    def do(self):
        """Sets running variable to False and brake the mainloop"""
        global running
        running = False


class ExitGameButton(Button):
    """
    Button which allows to exit the game while playing
        Inherit from the 'Button' class
    """
    def do(self):
        """Changes current screen to the game exit window"""
        global current_screen
        current_screen = gexit


class ReturnButton(Button):
    """
    Button which returns user to the current game if they tried to exit
        Inherit from the 'Button' class
    """
    def do(self):
        """Changes current screen to the game window"""
        global current_screen
        current_screen = game


class ChoiceSubmitButton(Button):
    """
    Button which submits amount of players and opens names screen
        Inherit from the 'Button' class
    """
    def do(self):
        """Changes current screen to the names window"""
        global current_screen, names
        names = Names()
        current_screen = names


class NamesSubmitButton(Button):
    """
    Button which submits players names and starts the game
        Inherit from the 'Button' class
    """
    def do(self):
        """Check uniqueness of names, save them and change current screen to the game window"""
        global current_screen, game
        game = Game()
        for field in names.fields:
            game.players_names.append(field.text)
        if len(set(game.players_names)) == len(game.players_names):  # Check weather all names are different
            game.player_number = choice.player_number
            current_screen = game
            game.start_the_game()
            with open(log_file_name, 'a') as log_file:
                print(f'\n\n__A new game was started\n', file=log_file)
        else:
            names.same_name_error = True
            with open(log_file_name, 'a') as log_file:
                print(f'\nError user tried to enter similar names is handled', file=log_file)


class DiceButton(Button):
    """
    Button which gives opportunity to roll dice
        Inherit from the 'Button' class
    """
    def do(self):
        global current_screen, game
        game.roll_dice()


def switch_screen(screen):
    """Triggers at the end of each pygame loop and displays current surface"""
    screen.draw()
    main_screen.blit(screen.surface, (0, 0))


# Creates class implementations
menu = Menu()
guide = Guide()
board = Leaderboard()
choice = Choice()
names = Names()
game = Game()
gexit = GameExit()
endgame = GameEnd()
current_screen = menu  # States starting window
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
