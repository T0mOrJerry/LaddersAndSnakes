# 引入pygame库和random库，用于图形界面显示和生成随机数
import pygame
import random

# 初始化pygame模块
pygame.init()
# 游戏主循环的运行标志
running = True
# 创建时钟对象，用于控制游戏帧率
clock = pygame.time.Clock()
# 设置游戏的帧率为60帧每秒
FPS = 60

# 定义窗口尺寸的常量
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# 键盘输入的键码到字符的映射字典
keys_codes = {48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 97: 'a',
              98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k',
              108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
              118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}

# 定义游戏中使用的颜色，每个颜色都有用于圆形和计分板的亮度不同的两种版本
colors = [[(237, 152, 152), (222, 35, 35)], [(189, 152, 237), (116, 35, 222)], [(152, 170, 237), (35, 76, 222)],
          [(152, 237, 237), (35, 222, 222)], [(152, 237, 196), (35, 222, 132)],
          [(169, 237, 152), (73, 222, 35)], [(220, 237, 152), (185, 222, 35)],
          [(237, 229, 152), (222, 203, 35)], [(237, 203, 152), (222, 147, 35)],
          [(237, 187, 152), (222, 113, 35)], [(237, 162, 152), (222, 57, 35)]]


# 定义棋盘格子的大小和棋盘的行列数
CELL_SIZE = 120
ROWS = 5
COLS = 8

# 定义不同的字体样式和大小
BigFont = pygame.font.SysFont("Arial", 60)
NormalFont = pygame.font.SysFont("Arial", 32)
TitleFont = pygame.font.SysFont("Arial", 100)
BodyFont = pygame.font.SysFont("Arial", 25)

# 创建一个用于记录游戏日志的文件
log_file_name = 'game_log.txt'
with open(log_file_name, 'w') as file:
    print('\t\t\t______LOGS OF THE CURRENT GAME______\n\n', file=file)


# 存储玩家数据的字典
players = {
    "Omar": [52, 430],
    "Alex": [63, 320],
    "Wilson": [54, 390]
}



# 创建多个用于不同界面显示的surface对象
main_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
menu_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
guide_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
leader_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
choice_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
names_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_exit_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_end_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



# 合并两个已排序的列表（left 和 right）并保持整体顺序
def merge(left, right):
    i = j = 0
    merged = []

    # 比较 left[i] 和 right[j] 的分数（列表中的第三个元素），并将较大的元素添加到结果列表 merged 中，然后移动相应的指针。
    while i < len(left) and j < len(right):
        if left[i][2] > right[j][2]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # 当一个列表的元素全部被添加到结果中后，将另一个列表的剩余元素添加到结果列表中
    merged += left[i:]
    merged += right[j:]
    return merged


# 将列表分割和合并排序
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    return merge(left_sorted, right_sorted)

# 将玩家数据的字典转换为列表，以便于进行排序。
def dict_list(di: dict) -> list:
    li = []

    # 对于每个键值对，创建一个元组（玩家名，第一个分数，第二个分数）并添加到列表中。
    for i in di:
        li.append((i, di[i][0], di[i][1]))
    return li


# 将排序后的列表转换回字典格式。
def list_dict(li: list) -> dict:
    di = {}
    for i in li:
        di[i[0]] = [i[1], i[2]]
    return di


# 将字典格式的玩家数据排序，并处理可能发生的任何异常。
def dict_merge_sort(di: dict) -> dict:
    try:  # Error handling if for some reason(later we make it impossible) exception occurred
        result = list_dict(merge_sort(dict_list(di)))
        return result
    except Exception as exception:
        with open(log_file_name, 'a') as log_file:
            print(f'\n!!!!ERROR!!! {type(exception).__name__} occurred', file=log_file)


# 管理游戏中玩家的顺序
class Queue:
    def __init__(self):
        self.items = []
        self.ln = 0

    # 将一个元素加入队列的起始位置。
    def enqueue(self, val):
        self.items.insert(0, val)


    # 从队列的末尾移除一个元素并返回它，如果队列为空，则返回 None。
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop()

    # 返回队列末尾的元素但不移除它，如果队列为空，则返回 None。
    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.items[-1]


    # 检查队列是否为空。
    def is_empty(self):
        return len(self.items) == 0


    def __str__(self):  # This function was created for debugging to correctly display the queue
        return ', '.join(list(map(str, self.items)))


    # 返回队列中的元素数量。
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




# 游戏板上的单个格子，它存储了格子的位置（行和列）、值和索引，以及与其他格子的连接（如梯子或蛇的头和尾）。
class Cell:
    def __init__(self, row, col, val, index):
        self.row = row
        self.col = col
        self.val = val
        self.index = index
        self.connections = []

    # 添加与其他格子的连接，这些连接代表游戏中的蛇或梯子，允许玩家从一个格子直接移动到另一个格子。
    def add_connection(self, neighbor):
        self.connections.append(neighbor)

    def __str__(self):
        return f"{self.row}, {self.col}, {self.index}, {self.val}"




# 游戏菜单界面的核心，负责呈现和处理与菜单相关的用户交互。
class Menu:

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


    # 在屏幕上绘制菜单的内容，包括按钮和标题。
    def draw(self):
        self.surface.fill('white')
        btn_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        for button in self.buttons:  # This draws each button on the screen
            button.draw()


    # 处理用户的点击事件，例如，当用户点击按钮时，执行相应的动作。
    def check(self, user_event):
        for button in self.buttons:
            button.check(user_event)


# 选择游戏中玩家数量的窗口
class Choice:


    def __init__(self):
        """Initialise window and states all essential properties"""
        self.surface = choice_screen  # everything in choice class will be in the choice_screen surface

        # 存储当前用户选择的玩家数量，默认为1
        self.player_number = 1

        # 创建按钮数组，包括增加和减少玩家数的按钮（ArrowUpButton 和 ArrowDownButton）、退出按钮（ExitButton）和提交按钮（ChoiceSubmitButton）。这些按钮都有特定的位置、大小和颜色。
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


    # 在屏幕上绘制选择窗口的内容，包括文本和按钮。
    def draw(self):

        # 填充窗口背景为白色。
        self.surface.fill('white')

        # 绘制页面标题和选择玩家数量的提示文本。
        page_txt = TitleFont.render("Snakes & Ladders", True, "Black", None)
        r = page_txt.get_rect()
        self.surface.blit(page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 15))
        small_page_txt = BigFont.render("Choose amount of players", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))

        # 显示当前选择的玩家数量，使用矩形框突出显示，并在其中心绘制玩家数量。
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

# 管理玩家输入名字的界面。
class Names:


    # 初始化窗口，创建退出和提交按钮，以及根据选择的玩家数量创建输入字段。
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


    # 绘制界面，包括按钮、输入字段和相关文本。如果存在命名错误（例如重复的名字），则显示错误消息。
    def draw(self):
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

    # 处理从键盘的输入，允许玩家在输入字段中输入名字。
    def inp(self, user_event):
        for field in self.fields:
            field.inp(user_event)


# 用于显示游戏指南，目前只有退出按钮的基本实现。
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


    # 绘制界面，显示“Guide”标题和按钮。
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


# 显示游戏的排行榜，展示玩家的成绩和排名。
class Leaderboard:

    # 初始化界面和退出按钮。
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


    # 在屏幕上指定位置添加文本。
    def add_text(self, txt, wid, hig, color=(227, 190, 148)):
        """Adds text in the stated positions in the surface"""
        body_surface = BodyFont.render(str(txt), True, color)
        self.surface.blit(body_surface, (wid, hig))


    # 绘制单个玩家的排名、玩家名称、游戏轮数和得分。
    def result(self, li, di, i, y):
        pygame.draw.line(self.surface, (102, 61, 14), (0, y), (WINDOW_WIDTH, y), 50)
        self.add_text(str(i + 1), 0, y + self.bodyheight / 2 - 25)
        self.add_text(str(li[i]), WINDOW_WIDTH / 4 - 100, y + self.bodyheight // 2 - 25)
        self.add_text(str(di[li[i]][0]), WINDOW_WIDTH / 2 - 100, y + self.bodyheight / 2 - 25)
        self.add_text(str(di[li[i]][1]), WINDOW_WIDTH - 100, y + self.bodyheight / 2 - 25)

    # 绘制整个排行榜界面，包括排名、玩家名、游戏轮数和得分。
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


# 用于填充游戏屏幕内容，以便在主循环中显示。
class Game:


    def __init__(self):
        """Initialises window and states all essential properties"""
        self.surface = game_screen

        #  添加退出游戏按钮和掷骰子按钮
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

        # 初始化玩家顺序队列
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


    #  结束游戏
    def end_game(self):


        # 更新全局字典，存储玩家的分数用于排行榜
        global current_screen, players
        self.finished = True

        # 更新玩家分数信息
        for name in self.player_score:

            # 如果玩家不在全局玩家列表中，将其添加进去
            if name not in players:
                players[name] = [self.turns // len(self.players_names) + 1, self.player_score[name]]
            else:

                # 累加玩家的回合数和分数
                players[name][0] += self.turns // len(self.players_names) + 1
                players[name][1] += self.player_score[name]

        # 胜利者额外得到50分
        players[self.players_order.peek()][1] += 50  # The winner takes 50 extra points
        current_screen = endgame


    # 绘制并更新右上角的当前得分信息
    def draw_score(self):

        start_position = (WINDOW_WIDTH / 5 * 4, 0)
        k = 0


        #  根据玩家顺序绘制得分板
        for player in self.players_order:
            score = self.player_score[player]

            # 绘制矩形框和得分信息
            pygame.draw.rect(self.surface, self.players_colors[player][0],
                             (start_position[0], start_position[1] + k, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 17))
            btn_txt = BodyFont.render(f'{player}:      {score}', True, "Black", None)
            r = btn_txt.get_rect()
            self.surface.blit(btn_txt,
                              (start_position[0] + 10, start_position[1] + k + (WINDOW_HEIGHT / 17 - r.height) / 2))
            k += WINDOW_HEIGHT // 17

        # 显示当前玩家的回合信息
        turn_txt = NormalFont.render(f"{self.players_order.peek()}'s turn", True, "Black", None)
        cr = turn_txt.get_rect()
        self.surface.blit(turn_txt,
                          (WINDOW_WIDTH / 5 * 4 + (WINDOW_WIDTH / 5 - cr.width) / 2,
                           start_position[1] + k + (WINDOW_HEIGHT / 17 - cr.height) / 2))


    # 创建掷骰子的界面
    def draw_dice_screen(self):

        # 绘制掷骰子的空间
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (WINDOW_WIDTH / 5 * 4, WINDOW_HEIGHT / 17 * 5, WINDOW_WIDTH / 5,
                          WINDOW_HEIGHT / 3 * 2 - WINDOW_HEIGHT / 7 * 2),
                         width=5)

        # 如果有掷骰子的表面存在，则绘制
        if self.dice_surface is not None:
            self.surface.blit(self.dice_surface, (self.dice_pos_x, self.dice_pos_y))


    # 根据掷骰子的结果绘制相应的骰子图像, value为掷骰子的结果值。
    def draw_dice(self, value):

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


    # 掷骰子动画函数，当按下掷骰子按钮时执行
    def dice_animation(self):

        for i in range(random.randrange(10, 20)):  # The amount of frames for animation is randomly picked
            self.dice_pos_x = WINDOW_WIDTH / 5 * 4 + 10 + random.randrange(0, WINDOW_WIDTH // 5 - 20 - self.dice_size)
            self.dice_pos_y = WINDOW_HEIGHT / 17 * 5 + 10 + random.randrange(0,
                                                                             WINDOW_HEIGHT // 3 * 2 - WINDOW_HEIGHT //
                                                                             7 * 2 - 20 - self.dice_size)
            self.draw_dice(random.randrange(1, 7))
            pygame.time.wait(150)  # The function freezes the program for a bit so the animation can be noticed
        self.draw_dice(self.dice_value)


    # 绘制玩家在游戏板上的位置
    def draw_players(self):

        k_x = CELL_SIZE / 4
        k_y = CELL_SIZE / 4
        c = 0

        # 计算玩家的绘制位置
        for player in self.players_names:
            h_x = 20 + self.players_positions[player][1] * CELL_SIZE + k_x
            h_y = 40 + self.players_positions[player][0] * CELL_SIZE + k_y

            # 绘制代表玩家的圆形
            pygame.draw.circle(self.surface, self.players_colors[player][1], (h_x, h_y), CELL_SIZE / 8)

            # 切换绘制位置，以便让玩家图形错落有致
            if c % 2 == 0:
                k_x += CELL_SIZE / 2
                k_x %= CELL_SIZE
            else:
                k_y += CELL_SIZE / 2
                k_x %= CELL_SIZE
            c += 1


    # 当玩家掷骰子后，移动玩家的圆圈
    def move(self):

        player = self.players_order.peek()
        h_x = self.players_positions[player][1]
        h_y = self.players_positions[player][0]


        print("回合数：", self.turns)
        print("当前玩家：", self.players_order.peek(), end="\t ")
        print("之前位置：", self.players_positions[player][0], self.players_positions[player][1])
        print("之前分数：", self.player_score[player])
        print("骰子点数：", self.dice_value, end="\t ")


        # 如果玩家无法移动到任何地方且处于游戏板边缘，则结束游戏
        if h_y == 0 and h_x + self.dice_value >= COLS:
            self.end_game()
        else:

            #  如果当前位置与掷骰子结果可以移动到下一列且在偶数行上
            if h_x + self.dice_value < COLS and h_y % 2 == 0:
                self.players_positions[player][1] += self.dice_value

            # 如果当前位置与掷骰子结果可以移动到上一列且在奇数行上
            elif h_x - self.dice_value >= 0 and h_y % 2 == 1:
                self.players_positions[player][1] -= self.dice_value

            # 如果当前位置在偶数行上，则向上移动一行并更新列位置
            elif h_y % 2 == 0:
                self.players_positions[player][0] -= 1
                self.players_positions[player][1] = COLS - (self.dice_value - (COLS - h_x)) - 1

            # 如果当前位置在奇数行上，则向上移动一行并更新列位置
            elif h_y % 2 == 1:
                self.players_positions[player][0] -= 1
                self.players_positions[player][1] = self.dice_value - h_x - 1

            # 检查当前位置是否与梯子或蛇相连，进行相应位置的更新
            connected = self.game_board.cells[self.players_positions[player][0]][
                self.players_positions[player][1]].connections
            if connected:

                # 如果当前位置与另一个单元格通过梯子或蛇相连，则更新位置
                if connected[0] is not None:
                    self.players_positions[player][0] = connected[0].row
                    self.players_positions[player][1] = connected[0].col

            # 更新玩家分数
            self.player_score[player] += self.game_board.cells[self.players_positions[player][0]][
                self.players_positions[player][1]].val


            print("所得分数：", self.game_board.cells[self.players_positions[player][0]][self.players_positions[player][1]].val)
            print("现在位置：", self.players_positions[player][0], self.players_positions[player][1], end="\t ")
            print("现在分数：", self.player_score[player])

    # 绘制函数，绘制并贴图所有游戏界面上的元素
    def draw(self):

        # 清空游戏界面为白色
        self.surface.fill('white')

        # 绘制游戏板
        self.game_board.draw_board()

        # 绘制所有按钮
        for button in self.buttons:
            button.draw()

        # 绘制得分信息
        self.draw_score()

        # 绘制掷骰子界面
        self.draw_dice_screen()

        # 将游戏板贴图到界面上（带偏移量，以便在屏幕上适当显示）
        self.surface.blit(self.game_board.surface, (20, 40))

        # 绘制玩家在游戏板上的位置
        self.draw_players()


    # 点击 'Roll The die' 按钮时调用
    def roll_dice(self):

        # 随机选择1到6之间的整数，模拟掷骰子的结果
        self.dice_value = random.choice([1, 2, 3, 4, 5, 6])  # States final die result

        # 播放掷骰子动画
        self.dice_animation()

        # 更新玩家回合数
        self.turns += 1

        # 移动玩家的位置
        self.move()

        # 记录游戏日志
        with open(log_file_name, 'a') as log_file:
            print(f'Turn {self.turns}; Player: {self.players_order.peek()}; Die rolled: {self.dice_value}; '
                  f'New player position: {self.players_positions[self.players_order.peek()]}', file=log_file)

        # 如果游戏未结束，继续下一位玩家的轮换
        if not self.finished:  # Stops players' rotation when the game is over
            self.players_order.enqueue(self.players_order.dequeue())

    def check(self, user_event):

        # 遍历所有按钮，检查用户事件是否与按钮交互
        for button in self.buttons:
            button.check(user_event)

    # 开始游戏
    def start_the_game(self):

        # # 初始化并创建游戏板
        self.game_board = Board()

        # 设置游戏板左下角单元格的值为0
        self.game_board.cells[ROWS - 1][0].val = 0

        # 将输入的玩家名称添加到游戏中
        for name in self.players_names:
            self.player_score[name] = 0

        # 创建玩家顺序的队列
        for name in list(set(self.players_names)):
            self.players_order.enqueue(name)

        # 随机分配玩家与颜色的关联
        for color, player in zip(random.sample(colors, self.player_number), self.players_names):
            self.players_colors[player] = color

        # 设定所有玩家的起始位置为游戏板左下角
        for player in self.players_names:  # States starting position for all players
            self.players_positions[player] = [ROWS - 1, 0]  # Left bottom cell is the beginning


# 创建并绘制棋盘
class Board:


    def __init__(self):
        # 初始化窗口并声明所有必要的属性
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

                # 随机生成单元格的值，范围在 -35 到 50 之间
                self.cells[row].append(Cell(row, col, random.randrange(-35, 50), index))
        self.create_ladders()
        self.create_snakes()


    # 创建梯子（连接两个单元格，形成一条棕色线）
    def create_ladders(self):

        k = 0
        # 棋盘中不能少于2个梯子
        while k < 2:
            # 梯子的数量是随机的 - 在2到6之间
            for i in range(random.randrange(3, 5)):
                # 随机选择要连接的单元格
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

    # 创建蛇（连接两个单元格，形成一条绿色线）
    def create_snakes(self):

        # 棋盘中不能少于2个蛇
        t = 0
        while t < 2:

            # 蛇的数量是随机的 - 在2到6之间
            for i in range(random.randrange(3, 5)):

                # 随机选择要连接的单元格
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

    # 绘制棋盘，设置每个单元格的大小和在棋盘上的顺序
    def draw_board(self):

        # # 填充棋盘为浅灰色
        self.surface.fill((200, 200, 200))
        for row in range(self.rows):
            for col in range(self.cols):

                # 棋盘的颜色
                if (row + col) % 2 == 0:
                    color = (139, 189, 120)
                else:
                    color = (200, 200, 200)
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.surface, color, rect)

        # 绘制梯子和蛇（线条）
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].connections:
                    if self.cells[row][col].connections[0] is not None:
                        if self.cells[row][col].index < self.cells[row][col].connections[0].index:
                            # 梯子的颜色为棕色
                            line_color = (102, 61, 14)
                        else:
                            # 蛇的颜色为绿色
                            line_color = (26, 107, 39)
                        b_row = self.cells[row][col].connections[0].row
                        b_col = self.cells[row][col].connections[0].col
                        x1, y1 = self.cells[row][col].col * CELL_SIZE + CELL_SIZE / 2, self.cells[row][
                            col].row * CELL_SIZE + CELL_SIZE / 2
                        x2, y2 = self.cells[b_row][b_col].col * CELL_SIZE + CELL_SIZE / 2, self.cells[b_row][
                            b_col].row * CELL_SIZE + CELL_SIZE / 2
                        pygame.draw.line(self.surface, line_color, (x1, y1), (x2, y2), 15)

        # 添加单元格编号和值信息
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


# 退出开始的游戏
class GameExit:

    def __init__(self):

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


    # 绘制屏幕上的所有内容
    def draw(self):

        self.surface.fill('white')
        small_page_txt = BigFont.render("Are you sure you want to exit the game?", True, "Black", None)
        r = small_page_txt.get_rect()
        self.surface.blit(small_page_txt, ((WINDOW_WIDTH - r.width) / 2, WINDOW_HEIGHT / 4))

        # 绘制每个按钮
        for button in self.buttons:  # This draws each button on the screen
            button.draw()

    def check(self, user_event):
        """Execute every user request"""
        for button in self.buttons:
            button.check(user_event)

# 游戏结束并显示游戏结果
class GameEnd:

    def __init__(self):

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


# 模拟输入框
class EnterField:

    def __init__(self, surf, width: float, height: float, pos_x: float, pos_y: float, text=''):

        self.surface = surf
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.activated = False


    # 绘制输入框
    def draw(self):


        if not self.activated:
            pygame.draw.rect(self.surface, "gray", (self.pos_x, self.pos_y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, "white", (self.pos_x, self.pos_y, self.width, self.height))
        pygame.draw.rect(self.surface, "black", (self.pos_x, self.pos_y, self.width, self.height), width=2)
        btn_txt = NormalFont.render(self.text, True, 'black', None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, (self.pos_x + 5, self.pos_y + (self.height - r.height) / 2))

    # 处理输入框被点击的事件
    def check(self, *args):

        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):
            if args[0].type == 1025:
                self.activated = not self.activated
        elif self.activated and args[0].type == 1025:
            self.activated = not self.activated


    # 处理从键盘接收的输入
    def inp(self, *args):

        if self.activated:
            if 97 <= args[0].key <= 122 or 48 <= args[0].key <= 57:
                if not self.text:
                    self.text += keys_codes[args[0].key].upper()
                elif len(self.text) <= 27:
                    self.text += keys_codes[args[0].key]
            elif args[0].key == 8:  # Text can be deleted with 'Delete' button in the keyboard
                self.text = self.text[:-1]


# 按钮(检查鼠标点击，处理按钮被按下的事件，并触发按钮的操作)
class Button:

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


    # 添加按钮文本
    def add_txt(self):
        btn_txt = NormalFont.render(self.text, True, self.txt_color, None)
        r = btn_txt.get_rect()
        self.surface.blit(btn_txt, (self.pos_x + (self.width - r.width) / 2, self.pos_y + (self.height - r.height) / 2))

    # 处理鼠标点击按钮
    def check(self, *args):

        p = args[0].pos
        if (self.pos_x <= p[0] <= self.pos_x + self.width) and (self.pos_y <= p[1] <= self.pos_y + self.height):

            # 区分用户按下和释放按钮的行为
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


    # 定制按钮
    def do(self):
        """
        This function is empty for the template
            It is personalized for different buttons and reliable for button's job
        """
        pass

# 开始游戏的按钮
class StartButton(Button):

    def add_txt(self):
        super().add_txt()
        self.draw_snake()  # This button has a unique design with a snake


    # 在按钮上绘制蛇形图案
    def draw_snake(self):

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

    # 切换当前屏幕到选择窗口
    def do(self):

        global current_screen
        choice.player_number = 1  # By default, number of players is 1
        current_screen = choice


class BoardButton(Button):


    # 切换当前屏幕到排行榜窗口
    def do(self):

        global current_screen, players
        players = dict_merge_sort(players)
        current_screen = board


# 打开游戏指南的按钮
class GuideButton(Button):


    # 切换当前屏幕到游戏指南窗口
    def do(self):

        print("Let's learn how to play")
        global current_screen
        current_screen = guide

# 增加玩家数量
class ArrowUpButton(Button):


    # 绘制带有箭头的三角形按钮
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


    # 处理鼠标点击箭头按钮的事件
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

    # 增加玩家数量
    def do(self):

        choice.player_number = choice.player_number % 4 + 1

# 减少玩家数量的按钮
class ArrowDownButton(Button):

    def draw(self):

        # 绘制带有箭头的三角形按钮
        if not self.pressed:
            pygame.draw.polygon(self.surface, 'black', [(self.pos_x + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width + 4, self.pos_y + 4),
                                                        (self.pos_x + self.width / 2 + 4,
                                                         self.pos_y + self.height + 4)])
        pygame.draw.polygon(self.surface, self.btn_color, [(self.pos_x, self.pos_y),
                                                           (self.pos_x + self.width, self.pos_y),
                                                           (self.pos_x + self.width / 2, self.pos_y + self.height)])

    # 处理鼠标点击箭头按钮的事件
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


    # 减少玩家数量
    def do(self):

        choice.player_number = choice.player_number - 1
        if choice.player_number == 0:
            choice.player_number = 4

# 返回到菜单屏幕的按钮
class ExitButton(Button):

    def do(self):

        # 切换当前屏幕到菜单窗口
        global current_screen
        current_screen = menu


# 允许退出应用程序并停止运行
class ExitAppButton(Button):

    # 将运行状态变量设置为 False，中断主循环
    def do(self):
        """Sets running variable to False and brake the mainloop"""
        global running
        running = False

# 退出游戏
class ExitGameButton(Button):

    def do(self):

        # 切换当前屏幕到游戏退出窗口
        global current_screen
        current_screen = gexit


# 菜单返回到当前游戏的按钮
class ReturnButton(Button):

    def do(self):

        # 切换当前屏幕到游戏窗口
        global current_screen
        current_screen = game

# 提交玩家数量并打开名称屏幕的按钮
class ChoiceSubmitButton(Button):

    def do(self):

        # 切换当前屏幕到名称窗口
        global current_screen, names
        names = Names()
        current_screen = names

# 提交玩家名称并开始游戏的按钮
class NamesSubmitButton(Button):

    def do(self):

        # 检查名称的唯一性，保存它们并切换当前屏幕到游戏窗口
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

# 掷骰子的按钮
class DiceButton(Button):

    def do(self):
        global current_screen, game
        game.roll_dice()

# 在每次 pygame 循环结束时触发，并显示当前表面
def switch_screen(screen):

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
    for event in pygame.event.get():  # 获取所有当前的事件
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            current_screen.check(event)
        if event.type == pygame.KEYDOWN and current_screen == names:
            current_screen.inp(event)

    # 根据当前屏幕切换进行处理
    switch_screen(current_screen)
    pygame.display.flip()
    clock.tick(FPS)  #  控制每秒更新的帧数
pygame.quit()

