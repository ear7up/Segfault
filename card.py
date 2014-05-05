import pygame
import memory_cell
import screen

class Card:

    def __init__(self):
        pass

    def __init__(self, name, text, cost, function, path, isFunction = False, bytes = None, value = None):
        self.name = name
        self.text = text
        self.cost = cost
        self.bytes = bytes
        self.path = path
        self.img = pygame.image.load(path).convert_alpha()
        self.value = value
        self.posx = 0
        self.posy = 0
        self.functions = [function]
        self.isFunction = isFunction

    def play(self, game):
        if len(self.functions) > 0:
            a = True
            for f in self.functions:
                a = a and f(self, game, self.value)
            return a

    def __str__(self):
        return self.name + '\t' + str(self.cost) + '\n' + self.text + '\n(' + str(self.posx) + ',' + str(self.posy) + ')\n'

    def copy(self):
        c = Card(self.name, self.text, self.cost, None, self.path, self.isFunction, self.bytes, self.value)
        c.functions = self.functions
        return c

    def render(self, window, mousex, mousey):
        #pygame.draw.rect(screen.window, pygame.Color(255, 0, 0), (x, y, 96, 128))
        offset = 0
        if self.posx <= mousex <= self.posx + screen.CARD_WIDTH and self.posy <= mousey <= self.posy + screen.CARD_HEIGHT:
            offset = 8
        if mousey > 431:
            offset *= -1
        window.blit(self.img, (self.posx, self.posy+offset))
        #screen.flip()


    def int(self, game, value = None):
        i = self.getMemoryTarget(game)
        if i is None:
            return False
        return game.get_current_player().put_memory(i, value, 4) #cost, len in bytes

    def bool(self, game, value = None):
        i = self.getMemoryTarget(game)
        if i is None:
            return False
        return game.get_current_player().put_memory(i, value, 1) #cost, len in bytes

    def pointer(self, game, dlkfjsdl = None): # unused
        i = self.getMemoryTarget(game)
        if i is None:
            return False
        self.value = i

    def getMemoryTarget(self, game, both = False):
        if both:
            game.state = 6
        else:
            game.state = 3 # set the game state to "target memory"
        i = game.update()
        while i is None and (game.state == 3 or game.state == 6):
            i = game.update()
        return i

    def free(self, game, dlsjfd = None):
        i = self.getMemoryTarget(game, True)
        if i is None:
            return False
        if i >= len(game.get_current_player().memory):
            i -= len(game.get_current_player().memory)
            m = game.get_inactive_player().memory[i]
            #
            #if m.length == 4:
            #    m.length = 1
            #    m.color(game.current_player)
            #    m.length = 4
            m.color(game.current_player)
            game.get_inactive_player().null_memory(i)
        else:
            game.get_current_player().null_memory(i)
        return True

    def add(self, game, lsdfjdl = None):
        i = self.getMemoryTarget(game, False)
        if i is None:
            return False
        x = game.pop_stack()
        y = game.pop_stack()
        if x is not None and y is not None:
            return game.get_current_player().put_memory(i, x + y, 4)
        game.stack_underflow()
        return False

    def sub(self, game, lsdfjdl = None):
        i = self.getMemoryTarget(game, False)
        if i is None:
            return False
        x = game.pop_stack()
        y = game.pop_stack()

        if x is not None and y is not None:
            return game.get_current_player().put_memory(i, max(0, x - y), 4)
        game.stack_underflow()

    def add_esp(self, game, lsdkjfs = None):
        x = game.pop_stack()
        print x
        if x is None:
            game.stack_underflow()
            return False
        for i in range(0,x):
            s = game.pop_stack()
            if not s:
                game.stack_underflow()
                return False
        return True

    def draw(self, game, sdlfkjd = None):
        x = game.pop_stack()
        if not x:
            game.stack_underflow()
            return False
        if not x:
            return False
        p = game.get_current_player()
        if p.current_cycles - 2 - 2*x < 0:
            game.stack.append(x)
            return False
        p.draw_cards(x)
        p.current_cycles -= 2*x
        return True

    def inc(self, game, lsdfjdl = None):
        i = self.getMemoryTarget(game, True)
        if i is None:
            return False
        p = None
        if i >= len(game.get_current_player().memory):
            i -= len(game.get_current_player().memory)
            p = game.get_inactive_player()
        else:
            p = game.get_current_player()
        if p.memory[i].value is None:
            return False
        else:
            p.memory[i].value += 1
        return True

    def dec(self, game, lsdfjdl = None):
        i = self.getMemoryTarget(game, True)
        if i is None:
            return False
        p = None
        if i >= len(game.get_current_player().memory):
            i -= len(game.get_current_player().memory)
            p = game.get_inactive_player()
        else:
            p = game.get_current_player()
        if p.memory[i].value is None:
            return False
        else:
            p.memory[i].value -= 1
        return True

    def alloc(self, game, lsdfjdl = None):
        for m in game.get_inactive_player().memory:
            if m.value is None:
                m.value = 0
                m.color(game.current_player)
                return True
        game.state = 5
        return False

    def pop(self, game, lsdfjdl = None):
        v = game.pop_stack()
        if not v:
            game.stack_underflow()
            return False
        else:
            i = self.getMemoryTarget(game, False)
            if i is None:
                game.stack.append(v)
                return False
            p = game.get_current_player()
            return p.put_memory(i, v, 4)

    def segfault(self, game, sdlkjfsdl = None):
        game.win('Player ' + str(game.current_player) + ' has won the game by forcing Player ' + str(game.get_inactive_player().number) + ' to segfault.\nClick to restart.')

    def peek(self, game, s = None):
        p = game.get_current_player()
        if len(p.deck) < 3:
            return False
        c1 = p.deck[-1]
        c2 = p.deck[-2]
        c3 = p.deck[-3]
        posx = [c1.posx, c2.posx, c3.posx]
        posy = [c1.posy, c2.posy, c3.posy]
        c1.posy = 300
        c2.posy = 300
        c3.posy = 300
        c1.posx = 242
        c2.posx = 242 + 96 + 4
        c3.posx = 242 + 96*2 + 8
        c1.render(game.screen.window, 0, 0)
        c2.render(game.screen.window, 0, 0)
        c3.render(game.screen.window, 0, 0)
        game.screen.flip()
        mx = 0
        my = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.MOUSEMOTION:
                    mx, my = event.pos
                if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
                    if c1.posx <= mx <= c1.posx + screen.CARD_WIDTH and c1.posy <= my <= c1.posy + screen.CARD_HEIGHT:
                        game.get_current_player().current_cycles -= 2
                        game.get_current_player().hand.append(c1)
                        game.get_current_player().used_cards.append(c1)
                        del game.get_current_player().deck[-1]
                        game.get_current_player().hand.remove(self)
                        return False
                    if c2.posx <= mx <= c2.posx + screen.CARD_WIDTH and c2.posy <= my <= c2.posy + screen.CARD_HEIGHT:
                        game.get_current_player().current_cycles -= 2
                        game.get_current_player().hand.append(c2)
                        game.get_current_player().used_cards.append(c2)
                        del game.get_current_player().deck[-2]
                        game.get_current_player().hand.remove(self)
                        return False
                    if c3.posx <= mx <= c3.posx + screen.CARD_WIDTH and c3.posy <= my <= c3.posy + screen.CARD_HEIGHT:
                        game.get_current_player().current_cycles -= 2
                        game.get_current_player().hand.append(c3)
                        game.get_current_player().used_cards.append(c3)
                        del game.get_current_player().deck[-3]
                        game.get_current_player().hand.remove(self)
                        return False
                if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 3:
                    return False

    def rqst_cycl(self, game, sldkfjd = None):
        game.get_current_player().max_cycles += 1
        return True

    def forx(self, game, sdlkfjds = None):
        p = game.get_current_player()
        x = game.pop_stack()
        if x is None:
            game.stack_underflow()
            return False
        else:
            game.state = 8 # pick target card
            c = game.update()
            while c is None and game.state == 8:
                c = game.update()
            if c is None:
                game.stack.append(x)
                return False
            c = p.hand[c]
            if p.current_cycles -2 - 2*x*c.cost < 0 or not c.isFunction:
                game.stack.append(x)
                return False
            for _ in range(0,x):
                c.function(c, game, c.value)
            p.current_cycles -= 2*x*c.cost
            return True

    def static(self, game, flsdkjf = None):
        i = self.getMemoryTarget(game, False)
        if i is None:
            return False
        p = game.get_current_player()
        if p.memory[i].value is None:
            return False
        p.memory[i].static = True
        return True

    def optimize(self, game, flsdkjf = None):
        game.state = 8 # pick target card
        c = game.update()
        while c is None and game.state == 8:
            c = game.update()
        if c is None:
            return False
        cost = game.get_current_player().hand[c].cost
        game.get_current_player().hand[c].cost = cost - 3 if cost - 3 > 0 else 1
        return True

    def rescope(self, game, fsdlkfj = None):
        cp = game.get_current_player()
        ip = game.get_inactive_player()
        for i in range(0, len(cp.memory)):
            if not cp.memory[i].static:
                cp.null_memory(i)
        for j in range(0, len(ip.memory)):
            if not ip.memory[j].static:
                ip.null_memory(j)
        return True

    def loose_thrd(self, game, dfjdlkj = None):
        game.get_inactive_player().max_cycles -= 1
        game.get_inactive_player().current_cycles -= 1
        return True

    def block(self, game, dflkdjs = None):
        game.state = 8 # pick target card
        c = game.update()
        while c is None and game.state == 8:
            c = game.update()
        if c is None:
            return False
        c2 = game.get_current_player().hand[c]
        del game.get_current_player().hand[c]
        fs = c2.functions
        del c
        game.state = 8 # pick target card
        c = game.update()
        while c is None and game.state == 8:
            c = game.update()
        if c is None:
            return False
        c2 = game.get_current_player().hand[c]
        del game.get_current_player().hand[c]
        fs.extend(c2.functions)
        self.functions = fs
        return False

    def thread(self, game, sdlfksdj = None):
        game.state = 8
        c = game.update()
        while c is None and game.state == 8:
            c = game.update()
        if c is None:
            return False
        c = game.get_current_player().hand[c]
        if not c.isFunction:
            return False
        if len(game.get_current_player().threads) == 2:
            return False
        game.get_current_player().threads.append(c.copy())
        del c
        return True

# variables
INT1 = Card("Integer", 'An integer', 2, Card.int, 'int1card.png', False, bin(1)[2:], 1)
INT2 = Card("Integer", 'An integer', 2, Card.int, 'int2card.png', False, bin(2)[2:], 2)
INT3 = Card("Integer", 'An integer', 2, Card.int, 'int3card.png', False, bin(3)[2:], 3)
BOOL0 = Card("Bool", 'A boolean', 1, Card.bool, 'boolTcard.png', False, bin(0)[2:], 1)
BOOL1 = Card("Bool", 'A boolean', 1, Card.bool, 'boolFcard.png', False, bin(1)[2:], 0)

#POINTER = Card('Pointer', 'A pointer', 1, Card.pointer, 'pointer.png')

#functions
FREE = Card("Free", 'Remove a value from memory.', 2, Card.free, 'freecard.png')
#ADD = Card('Add', 'Set a cell to be x + y')

ADD = Card('Add', 'Add x and y', 2, Card.add, 'addcard.png', True)
#ADD.isFunction = True
SUB = Card('Sub', 'Sub y from x', 2, Card.sub, 'subcard.png', True)
#SUB.isFunction = True

INC = Card('Inc', 'Increment a var', 2, Card.inc, 'inccard.png')
DEC = Card('Dec', 'Decrement a var', 2, Card.dec, 'deccard.png')

ADD_ESP = Card('Add esp', 'Remove the top x elements of the stack', 2, Card.add_esp, 'addespcard.png', True)
#ADD_ESP.isFunction = True
DRAW = Card('Draw', 'Draw c cards', 2, Card.draw, 'drawcard.png', True)
#DRAW.isFunction = True

ALLOC = Card('Alloc', 'Place 1 byte anywhere in memory', 3, Card.alloc, 'alloccard.png', True)
#ALLOC.isFunction = True
SEGFAULT = Card('Segfault', 'Win the game', 70, Card.segfault, 'segfaultcard.png', True)
#SEGFAULT.isFunction = True
POP = Card('Pop', 'Put a value from the stack into your memory', 1, Card.pop, 'popcard.png')

PEEK = Card('Peek', 'Look at the top three card in your deck; pick one, put back the others', 2, Card.peek, 'peekcard.png')
RQST_CYCL = Card('Rqst_Cycl', 'Gain one maximum cycle', 4, Card.rqst_cycl, 'rqst_cyclcard.png', True)
#RQST_CYCL.isFunction = True

FOR = Card('For', 'Play target function x times', 2, Card.forx, 'forcard.png', True)
#FOR.isFunction = True
STATIC = Card('Static', 'Target varaible is immune to rescope', 0, Card.static, 'staticcard.png')
RESCOPE = Card('Rescope', 'Destroy ALL non-static variables', 9, Card.rescope, 'rescopecard.png')

OPTIMIZE = Card('Optimize', 'Reduce target card\'s cost by 3 (minimum 1)', 1, Card.optimize, 'optimizecard.png')
#OPTIMIZE.isFunction = True

LOOSE_THRD = Card('Runaway Thread', 'Spawn a useless thread to permanently decrease opponent\'s cycles by 1', 5, Card.loose_thrd, 'loose_thrdcard.png', True)
#LOOSE_THRD.isFunction = True

BLOCK = Card('Block', 'Execute two functions', 0, Card.block, 'blockcard.png', True)
#BLOCK.isFunction = True

THREAD = Card('Thread', 'Execute a function using unspent cycles', 2, Card.thread, 'threadcard.png')

CARDS = [THREAD, SEGFAULT, INT1, INT2, INT3, STATIC, BOOL0, LOOSE_THRD, OPTIMIZE, BOOL1, ADD, SUB, ADD_ESP, DRAW, STATIC, INC, DEC, DRAW, ALLOC, FREE, SEGFAULT, POP, PEEK, FOR, RQST_CYCL, OPTIMIZE, RESCOPE]

