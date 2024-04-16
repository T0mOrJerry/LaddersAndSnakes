# Preparing PyGame module to run the application
import pygame
pygame.init()
running = True
clock = pygame.time.Clock()
FPS = 60


# Initializing constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BigFont = pygame.font.SysFont("Arial", 60)
NormalFont = pygame.font.SysFont("Arial", 32)
TitleFont = pygame.font.SysFont("Arial", 100)


# Creating different surfaces for different purpose
# One general and one for each window
main_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
menu_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
guide_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
leader_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
choice_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Each window is described as a class, which draws everything, that must be drawn
# and helps to connect user and every interactive piece of the window
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
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
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
            ArrowUpButton(self.surface, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 7 * 4 - 20,
                        (200, 61, 14),
                        (227, 190, 148)),
            ArrowDownButton(self.surface, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 7 * 4 + 20,
                          (200, 61, 14),
                          (227, 190, 148)),
            ExitButton(self.surface, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 10, WINDOW_WIDTH / 11 * 9,
                          WINDOW_HEIGHT / 10 * 8,
                          (255, 0, 0),
                          (227, 190, 148), 'Exit'),
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
        page_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render("Chose amount of players", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))
        pygame.draw.rect(self.surface, (0, 0, 0), (WINDOW_WIDTH / 7 * 3, WINDOW_HEIGHT / 7 * 3, WINDOW_WIDTH / 7, WINDOW_HEIGHT / 7 * 2), width=5)
        counter_txt = TitleFont.render(f"{self.player_number}", True, "Black", None)
        r = counter_txt.get_rect()
        self.surface.blit(counter_txt, (WINDOW_WIDTH / 7 * 3 + (WINDOW_WIDTH / 7 - r.width) / 2, WINDOW_HEIGHT / 7 * 3 + (WINDOW_HEIGHT / 7 * 2 - r.height) / 2))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


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
                       (255, 0, 0),
                       (227, 190, 148), 'Exit'),
        ]

    # This function draws everything, which will be on the screen
    def draw(self):
        btn_txt = TitleFont.render("Guide", True, "Black", None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):  # Execute every user request
        for button in self.buttons:
            button.check(user_event)


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
        print("Let's play!")
        global current_screen
        current_screen = choice


class BoardButton(Button):  # Class for the button which opens window of leaderboard
    def do(self):
        print("Let's see our leaders")


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


# "Switch screen" function which triggers at the end of each pygame loop and displays current surface
def switch_screen(screen):
    sc = screen.surface
    sc.fill('white')
    screen.draw()
    main_screen.blit(sc, (0, 0))
    pygame.display.flip()


menu = Menu()
guide = Guide()
choice = Choice()
current_screen = menu
while running:  # Window cycle
    for event in pygame.event.get():  # Event check
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            current_screen.check(event)
    switch_screen(current_screen)
    clock.tick(FPS)  # Setting the amount of frames per seconds (limits of updates per second)
pygame.quit()
