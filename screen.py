import pygame
pygame.font.init()
#FONT = pygame.font.Font('Tazz5x5.ttf', 16)
FONT = pygame.font.Font('courbd.ttf', 16)

WIDTH = 1152
HEIGHT = 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

CYCLE_XOFFSET = 1032
PLAYER1_CYCLE_YOFFSET = 435
PLAYER2_CYCLE_YOFFSET = 315

PLAYER1_Y_OFFSET = 620
PLAYER2_Y_OFFSET = 20
CARD_X_OFFSET = 18
CARD_WIDTH = 96
CARD_HEIGHT = 128
DISTNACE_BETWEEN_CARDS = 3

Y_DISTANCE_BETWEEN_MEMORY_CELLS = 8
MEMORY_CELL_WIDTH = 74
MEMORY_CELL_HEIGHT = 32
MEMORY_CELL_X_OFFSET = 49
PLAYER1_MEM_Y_OFFSET = 430
PLAYER2_MEM_Y_OFFSET = 178
X_DISTANCE_BETWEEN_CELLS = 16

#BACKGROUND = pygame.image.load('background.png')
#STATIC_UI = pygame.image.load('template.png')
BACKGROUND_UI = pygame.image.load('template.png').convert()
WIN_SCREEN = pygame.image.load('end_screen.png').convert()
CARD_BACK2 = pygame.image.load('back1.png').convert_alpha()
CARD_BACK1 = pygame.image.load('back2.png').convert_alpha()

class Screen:
    def __init__(self):
        pygame.init()
        self.window = WINDOW#pygame.display.set_mode((1152,768), pygame.locals.SRCALPHA)
        #STATIC_UI.convert_alpha()
        self.window.fill(pygame.Color(255,255,255))
        self.window.blit(BACKGROUND_UI, (0,0))
        #self.window.blit(STATIC_UI, (0,0))
        pygame.display.set_caption('Segfault: The Video Game')

        pygame.display.update()

    def flip(self):
        pygame.display.update()

    def render_hand(self, player, current, playerno, mousex, mousey, between):
        #y_offset different between players 1 and 2
        x_offset = 0
        if playerno == 1:
            y_offset = PLAYER1_Y_OFFSET
        else:
            y_offset = PLAYER2_Y_OFFSET
        if current and not between: #render front
            for card in player.hand:
                card.posx = CARD_X_OFFSET + x_offset
                card.posy = y_offset
                card.render(self.window, mousex, mousey)
                x_offset += CARD_WIDTH + DISTNACE_BETWEEN_CARDS
        else: #render backs
            for card in player.hand:
                card.posx = CARD_X_OFFSET + x_offset
                card.posy = y_offset
                img = None
                if playerno == 1:
                    img = CARD_BACK1
                elif playerno == 2:
                    img = CARD_BACK2
                self.window.blit(img, (card.posx, card.posy))
                x_offset += CARD_WIDTH + DISTNACE_BETWEEN_CARDS

    def render_memory(self, player):
        for mem in player.memory:
            mem.render(self.window)

    def render_cycles(self, player):
        tc = FONT.render('Cycles:', 1, (15,15,230))
        text = FONT.render('(' + str(player.current_cycles) + '/' + str(player.max_cycles) + ')', 1, (15, 15, 230))
        if player.number == 1:
            self.window.blit(tc, (CYCLE_XOFFSET+25, PLAYER1_CYCLE_YOFFSET-16))
            self.window.blit(text, (CYCLE_XOFFSET+30, PLAYER1_CYCLE_YOFFSET))

            d40 = FONT.render('30', 1, (15,15,230))
            self.window.blit(d40, (CYCLE_XOFFSET-59, PLAYER1_CYCLE_YOFFSET+255))

            o40 = FONT.render(str(len(player.deck)), 1, (15,15,230))
            self.window.blit(o40, (CYCLE_XOFFSET-59, PLAYER1_CYCLE_YOFFSET+220))

        elif player.number == 2:
            self.window.blit(tc, (CYCLE_XOFFSET+25, PLAYER2_CYCLE_YOFFSET))
            self.window.blit(text, (CYCLE_XOFFSET+30, PLAYER2_CYCLE_YOFFSET+16))

            d40 = FONT.render('30', 1, (15,15,230))
            self.window.blit(d40, (CYCLE_XOFFSET-59, PLAYER2_CYCLE_YOFFSET-220))

            o40 = FONT.render(str(len(player.deck)), 1, (15,15,230))
            self.window.blit(o40, (CYCLE_XOFFSET-59, PLAYER2_CYCLE_YOFFSET-260))




    def pad(self, x):
        l = 8 - len(str(x))
        return '0x' + '0'*l + str(hex(x)[2:])

    def render_stack(self, stack):
        yoffset = 574
        xoffset = 884 + 5
        for x in stack:
            text = FONT.render(self.pad(x), 0, (0,0,0))
            self.window.blit(text, (xoffset, yoffset))
            yoffset -= 16

    def render_win(self, win_msg):
        buffer = win_msg.split('\n')
        xoffset = WIDTH/2.0
        yoffset = HEIGHT/2.0 + 50
        self.window.blit(WIN_SCREEN, (0,0))
        for line in buffer:
            size = FONT.size(line)
            x = xoffset - 0.5*size[0]
            y = yoffset - 0.5*size[1]
            text = FONT.render(line, 0, (255, 255, 255))
            self.window.blit(text, (x,y))
            yoffset += size[1] + 2 # next line

    def render_threads(self, player):
        x = 1039
        y1 = 16
        y2 = 166
        y3 = 458
        y4 = 608

        if len(player.threads) >= 1:
            t1 = player.threads[0]
            t1.posx = x
            if player.number == 1:
                t1.posy = y3
            else:
                t1.posy = y1
            t1.render(self.window, 0, 0)
            left1 = t1.cost
            text1 = FONT.render(str(left1), 1, (255,0,0))
            self.window.blit(text1, (t1.posx + 45, t1.posy + 128))
        if len(player.threads) == 2:
            t2 = player.threads[1]
            t2.posx = x
            if player.number == 1:
                t2.posy = y4
            else:
                t2.posy = y2
            t2.render(self.window, 0, 0)
            left2 = t2.cost
            text2 = FONT.render(str(left2), 1, (255,0,0))
            self.window.blit(text1, (t2.posx + 45, t2.posy + 128))












