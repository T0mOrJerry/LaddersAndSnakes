import pygame

pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
BigFont = pygame.font.SysFont("Arial", 48)
NormalFont = pygame.font.SysFont("Arial", 32)
TitleFont = pygame.font.SysFont("Arial", 100)
running = True
current_window = 'MENU'


class Button:
    def __init__(self, width: float, height: float, pos_x: float, pos_y: float, color_brick: tuple,
                 color_text=(255, 255, 255), text=''):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.btn_color = color_brick
        self.txt_color = color_text
        self.text = text
        self.pressed = False

    def draw(self):
        if not self.pressed:
            pygame.draw.rect(screen, "black", (self.pos_x + 4, self.pos_y + 4, self.width, self.height))
        pygame.draw.rect(screen, self.btn_color, (self.pos_x, self.pos_y, self.width, self.height))
        self.add_txt()

    def add_txt(self):
        btn_txt = NormalFont.render(self.text, True, self.txt_color, None)
        r = btn_txt.get_rect()
        screen.blit(btn_txt, (self.pos_x + (self.width - r.width) / 2, self.pos_y + (self.height - r.height) / 2))

    def check(self, *args):
        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):
            if args[0].type == 1025:
                self.do()
                self.pressed = True
                self.pos_x += 4
                self.pos_y += 4
            elif args[0].type == 1026:
                self.pressed = False
                self.pos_x -= 4
                self.pos_y -= 4

    def do(self):
        print("Yes, Future!!!")


class StartButton(Button):
    def add_txt(self):
        btn_txt = BigFont.render(self.text, True, self.txt_color, None)
        r = btn_txt.get_rect()
        screen.blit(btn_txt, (self.pos_x + (self.width - r.width) / 2, self.pos_y + (self.height - r.height) / 2))
        self.draw_snake()

    def draw_snake(self):
        if not self.pressed:
            pygame.draw.rect(screen, "black", (self.pos_x - 20 + 4, self.pos_y + self.height - 8, 30, self.height + 85),
                             border_radius=20)
            pygame.draw.line(screen, "black", (self.pos_x + self.width + 70 + 4, self.pos_y + self.height + 65 + 4),
                             (self.pos_x + self.width + 90 + 4, self.pos_y + self.height + 65 + 4), width=3)
            pygame.draw.rect(screen, "black", (self.pos_x + self.width + 4, self.pos_y + self.height + 50 + 4, 70, 30),
                             border_radius=20)
        pygame.draw.rect(screen, (26, 107, 39), (self.pos_x - 20, self.pos_y - 25, 30, self.height + 200),
                         border_radius=20)
        pygame.draw.rect(screen, (26, 107, 39), (self.pos_x - 20, self.pos_y - 25, self.width + 50, 30),
                         border_radius=20)
        pygame.draw.rect(screen, (26, 107, 39), (self.pos_x + self.width, self.pos_y - 25, 30, self.height + 100),
                         border_radius=20)
        pygame.draw.line(screen, "red", (self.pos_x + self.width + 70, self.pos_y + self.height + 65),
                         (self.pos_x + self.width + 90, self.pos_y + self.height + 65), width=3)
        pygame.draw.rect(screen, (26, 107, 39), (self.pos_x + self.width, self.pos_y + self.height + 50, 70, 30),
                         border_radius=20)
        pygame.draw.circle(screen, "black", (self.pos_x + self.width + 60, self.pos_y + self.height + 59), radius=2)
        pygame.draw.circle(screen, "black", (self.pos_x + self.width + 60, self.pos_y + self.height + 71), radius=2)

    def do(self):
        print("Let's play!")


class BoardButton(Button):
    def do(self):
        print("Let's see our leaders")


class GuideButton(Button):
    def do(self):
        print("Let's learn how to play")


menu_buttons = [
    StartButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 7, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 7 * 4, (102, 61, 14),
                (227, 190, 148), 'Start'),
    BoardButton(WINDOW_WIDTH / 3.5, WINDOW_HEIGHT / 8, WINDOW_WIDTH / 11, WINDOW_HEIGHT / 7 * 5.045, (102, 61, 14),
           (227, 190, 148), 'Leaderboard'),
    GuideButton(WINDOW_WIDTH / 3.5, WINDOW_HEIGHT / 8, WINDOW_WIDTH / 8 * 5, WINDOW_HEIGHT / 7 * 3.08, (102, 61, 14),
           (227, 190, 148), 'User Guide'),
]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if current_window == 'MENU':
                for button in menu_buttons:
                    button.check(event)
    screen.fill("White")
    if current_window == 'MENU':
        btn_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = btn_txt.get_rect()
        screen.blit(btn_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        for button in menu_buttons:
            button.draw()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
