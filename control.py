import player
import screen
import card
import pygame
import random
from pygame.locals import *

states = {"START":1, "PICK_MOVE":2, "PICK_TARGET_MEMORY":3, "LOCKED":4, "WIN":5, "PICK_EITHER_MEMORY":6, "BETWEEN":7, "PICK_TARGET_CARD":8}
class Game:
    def __init__(self):
        self.between = False
        self.win_message = ''
        self.screen = screen.Screen()
        self.state = 1
        self.stack = []
        deck = [card.CARDS[int(i)].copy() for i in [random.random() * len(card.CARDS) for _ in range(40)]]
        self.player1 = player.Player(1, deck)
        self.player2 = player.Player(2, deck)
        self.current_player = 1

    def set_state(self, state):
        self.state = state

    def end_turn(self):
        if self.state != states["BETWEEN"]:
            self.between = True
            self.state = states["BETWEEN"]
        else:
            self.feed_threads(self.get_current_player().current_cycles)
            self.get_current_player().moved_this_turn = False
            if self.state != states["WIN"]:
                self.state = states["PICK_MOVE"]
            self.between = False
            if self.current_player == 1:
                self.current_player = 2
                c = self.player2.max_cycles + 1
                self.player2.max_cycles = c
                self.player2.current_cycles = c
                self.player2.draw_cards(1)
            else:
                self.current_player = 1
                c = self.player1.max_cycles + 1
                self.player1.max_cycles = c
                self.player1.current_cycles = c
                self.player1.draw_cards(1)

    def get_current_player(self):
        if self.current_player == 1:
            return self.player1
        else:
            return self.player2

    def get_inactive_player(self):
        if self.current_player == 1:
            return self.player2
        else:
            return self.player1

    def pop_stack(self):
        if len(self.stack) < 1:
            return None
        return self.stack.pop()

    def update(self):
        global mousex, mousey
        if self.state == states["START"]:
            initial_hand_size = 5
            self.player1.draw_cards(initial_hand_size)
            self.player2.draw_cards(initial_hand_size)
            self.set_state(states["PICK_MOVE"])

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.locals.QUIT))
                elif event.key == 13 and not self.state == 5:
                    self.end_turn()
                    #self.set_state(states["PICK_MOVE"])
            elif event.type == pygame.locals.MOUSEMOTION:
                mousex, mousey = event.pos
                #check end turn
                #(1041,363), (1131,405)
            elif event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
                if 1024 <= mousex <= 1131 and 363 <= mousey <= 405 and not self.state == 5:
                    self.end_turn()

            if game.state == states['WIN']:
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    self.reinit()
                    self.state = states["PICK_MOVE"]

            if game.state == states['PICK_TARGET_CARD']:
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        game.state = states["PICK_MOVE"]
                    else:
                        hand = game.get_current_player().hand
                        for i in range(0, len(hand)):
                        # if the click was within the boundary of a card, play that card
                            if hand[i].posx <= mousex <= hand[i].posx + screen.CARD_WIDTH and hand[i].posy <= mousey <= hand[i].posy + screen.CARD_HEIGHT:
                                game.state = states['PICK_MOVE']
                                return i if hand[i].isFunction else None

            # if the player is picking a card to play
            if game.state == states["PICK_MOVE"]:
                # if the player left clicks,
                if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
                    player = game.player1
                    if game.current_player == 1:
                        hand = game.player1.hand
                    else:
                        hand = game.player2.hand
                        player = game.player2

                    # check move
                    #(763, 372), (820,399)
                    if 763 <= mousex <= 820 and 372 <= mousey <= 399:
                        p = game.get_current_player()
                        if p.current_cycles >= 1 and not p.moved_this_turn:
                            po = game.get_inactive_player()
                            game.state = states["PICK_TARGET_MEMORY"]
                            i = game.update()
                            while i is None and game.state == states["PICK_TARGET_MEMORY"]:
                                i = game.update()
                            if i is not None:
                                m = p.get_memory(i)
                                if m.value is not None:
                                    moved = False
                                    for j in range(0, len(po.memory)):
                                        n = po.get_memory(j)
                                        if n.value is None and m.get_color() == game.current_player and po.put_memory(j, m.value, m.length):
                                            po.get_memory(j).color(game.current_player)
                                            p.current_cycles -= 1
                                            p.moved_this_turn = True
                                            game.state = states["PICK_MOVE"]
                                            moved = True
                                            break
                                    if not moved and m.get_color() == game.current_player:
                                        game.win('Player ' + str(self.current_player) + ' has won by overflowing his opponent\'s memory.\nClick to restart.')

                    # check push
                    #(928,162), (987, 190)
                    if 928 <= mousex <= 987 and 162 <= mousey <= 190:
                        game.state = states["PICK_TARGET_MEMORY"]
                        i = game.update()
                        while i is None and game.state == states["PICK_TARGET_MEMORY"]:
                            i = game.update()
                        if i is not None:
                            v = player.get_memory(i).value
                            if v is not None:
                                game.stack.append(player.get_memory(i).value)
                    if len(game.stack) > 25:
                        game.win('Player ' + str(game.get_inactive_player().number) + 'has won the game after Player ' + str(game.current_player) + ' overflowed the stack.\nClick to restart.' )
                    elif game.state != 5:
                        game.state = states["PICK_MOVE"]

                    for i in range(0, len(hand)):
                        # if the click was within the boundary of a card, play that card
                        if hand[i].posx <= mousex <= hand[i].posx + screen.CARD_WIDTH and hand[i].posy <= mousey <= hand[i].posy + screen.CARD_HEIGHT:
                            player.play(i, game)
                            break
            elif game.state == states["PICK_TARGET_MEMORY"] or game.state == states["PICK_EITHER_MEMORY"]:
                p = None
                l1 = None
                if game.state == states["PICK_TARGET_MEMORY"]:
                    p = game.get_current_player().memory
                else:
                    l1 = len(game.get_current_player().memory)
                    p = game.get_current_player().memory[:]
                    p.extend(game.get_inactive_player().memory)

                if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button ==1:
                    for i in range(0, len(p)):
                        m = p[i]
                        if m.posx <= mousex <= m.posx + 2*m.width and m.posy <= mousey <= m.posy + 2*m.height:
                            game.state = states["PICK_MOVE"]
                            return i
                if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 3:
                    game.state = states["PICK_MOVE"]
        return None

    def win(self, win_message):
        self.win_message = win_message
        self.state = states["WIN"]
        game.render()
        game.update()

    def stack_underflow(self):
        game.win('Player ' + str(game.get_inactive_player().number) + ' has won the game after Player ' + str(game.current_player) + ' underflowed the stack.\nClick to restart.' )

    def feed_threads(self, cycles):
        threads1 = self.player1.threads
        threads2 = self.player2.threads
        n = len(threads1) + len(threads2)
        if n == 0:
            n = 1
        cycles_per_thread = cycles/n
        for c1 in threads1:
            c1.cost -= cycles_per_thread
        for c2 in threads2:
            c2.cost -= cycles_per_thread
        self.check_threads()

    def check_threads(self):
        threads1 = self.player1.threads
        threads2 = self.player2.threads
        n = len(threads1) + len(threads2)
        for c1 in threads1:
            if c1.cost <= 0:
                for f in c1.functions:
                    f(c1, game, c1.value)
                threads1.remove(c1)
        for c2 in threads2:
            if c2.cost <= 0:
                for f in c2.functions:
                    f(c2, game, c2.value)
                threads2.remove(c2)

    def render(self):
        if self.state == states["WIN"]:
            self.screen.render_win(self.win_message)
        else:
            self.screen.window.blit(screen.BACKGROUND_UI, (0,0))
            #self.screen.window.blit(screen.STATIC_UI, (0,0))
            if self.current_player == 1:
                self.screen.render_hand(self.player1, True, 1, mousex, mousey, self.between)
                self.screen.render_hand(self.player2, False, 2, mousex, mousey, self.between)
            else:
                self.screen.render_hand(self.player1, False, 1, mousex, mousey, self.between)
                self.screen.render_hand(self.player2, True, 2, mousex, mousey, self.between)

            self.screen.render_memory(self.player1)
            self.screen.render_memory(self.player2)

            self.screen.render_cycles(self.player1)
            self.screen.render_cycles(self.player2)

            self.screen.render_stack(game.stack)

            self.screen.render_threads(self.player1)
            self.screen.render_threads(self.player2)

        self.screen.flip()

    def reinit(self):
        global game
        game = Game()
        game.screen = screen.Screen()


global game
game = Game()
s = screen.Screen()
game.screen = s

global mousex
mousex = 0

global mousey
mousey = 0

while 1:
    game.update()
    game.render()



