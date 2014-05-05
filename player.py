import random
import screen
import memory_cell

class Player:
    def __init__(self, number, deck):
        self.number = number
        self.moved_this_turn = False
        self.threads = []
        self.deck = deck
        self.used_cards = []
        random.shuffle(self.deck)
        self.hand = []
        self.memory = [None]*32
        xpos = screen.MEMORY_CELL_X_OFFSET
        if number == 1:
            ypos = screen.PLAYER1_MEM_Y_OFFSET
        else:
            ypos = screen.PLAYER2_MEM_Y_OFFSET
        for i in range(0,4):
            for j in range(0,8):
                self.memory[8*i + j] = memory_cell.Cell(xpos, ypos, 1, number)
                xpos += screen.X_DISTANCE_BETWEEN_CELLS + screen.MEMORY_CELL_WIDTH
            ypos += screen.MEMORY_CELL_HEIGHT + screen.Y_DISTANCE_BETWEEN_MEMORY_CELLS
            xpos = screen.MEMORY_CELL_X_OFFSET

        self.max_cycles = 2
        self.current_cycles = self.max_cycles

    def draw_cards(self, x):
        for i in range(0,x):
            if len(self.deck) == 0:
                self.deck = self.used_cards
                random.shuffle(self.deck)
                self.used_cards = []
            if len(self.hand) < 8:
                self.hand.append(self.deck[-1])
            self.used_cards.append(self.deck.pop())


    def play(self, i, game):
        if self.current_cycles >= self.hand[i].cost and self.hand[i].play(game): # returns if card was successfully played (may be cancelled)
            self.current_cycles -= self.hand[i].cost
            self.hand.pop(i)

    def get_memory(self, i):
        return self.memory[i]

    def put_memory(self, i, v, l):
        if i + l - self.memory[i].length < len(self.memory):
            x = self.memory[i].posx
            k = 0
            z = 0
            while k < l:
                k += self.memory[i+z].length
                z += 1
            if k > l:
                return False

            if self.memory[i+z-1].posy != self.memory[i].posy:
                return False
            k = 0
            while k < l-1:
                k += self.memory[i].length
                if k < l:
                    del self.memory[i]
            self.memory[i].length = l
            self.memory[i].posx = x
            self.memory[i].value = v
            if self.number == 1:
                self.memory[i].img = memory_cell.FOUR_BYTES_BLUE if l == 4 else memory_cell.ONE_BYTE_BLUE
            else:
                self.memory[i].img = memory_cell.FOUR_BYTES_RED if l == 4 else memory_cell.ONE_BYTE_RED
            self.memory[i].width = 4*memory_cell.CELL_WIDTH + 3 * screen.DISTNACE_BETWEEN_CARDS if l == 4 else memory_cell.CELL_WIDTH
            return True
        return False

    def null_memory(self, i):
        m = self.memory[i]
        m.value = None
        if m.length == 4:
            m.length = 1
            m.img = memory_cell.ONE_BYTE_BLUE if self.number == 1 else memory_cell.ONE_BYTE_RED
            xpos = m.posx
            ypos = m.posy
            xoffset = screen.MEMORY_CELL_WIDTH + screen.X_DISTANCE_BETWEEN_CELLS

            self.memory.insert(i+1, memory_cell.Cell(xpos + 3*xoffset, ypos, 1, m.get_color()))
            self.memory.insert(i+1, memory_cell.Cell(xpos + 2*xoffset, ypos, 1, m.get_color()))
            self.memory.insert(i+1, memory_cell.Cell(xpos + xoffset, ypos, 1, m.get_color()))

    def __str__(self):
        s = ""
        for card in self.deck:
            s += str(card) + '\n'
        return s
