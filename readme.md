
*** Segfault: The Video Game ***

You are a process running in an Operating System without proper memory isolation. As such, you can claim memory from other processess! 
Steal the enemy process' memory before he takes yours. If you have no space left in memory, you will be terminated. 
You also need to be careful. Do not overflow or underflow the stack.
Good Luck.

Installation
    Segfault requires PyGame, which can be found at http://www.pygame.org/download.shtml
    To run Segfault, run control.py with Python 2.7 

How to Play:

* Cycles
    You start with 2 cycles. Each turn you gain one maximum cycle and your cycles are refilled.
    Playing cards costs cycles, indicated by the number in a blue box on each card (some cards may also have conditional costs).

* Memory
    Each turn you may move (copy) one item from your memory into the first available spot in your opponent's memory. This costs 1 cycle.
    A player can win by overflowing up your opponent's memory.

* The Stack
    You can push values as many values as you want from your memory to the stack, all for free.
    Most function cards you play use the values on the top of the stack.
    The stack is shared between both players
    Trying to pop values from the stack when none are on it will cause you to lose.
    Trying to push more than 25 values to the stack will cause you to lose.

* Threads
    You can thread some functions to pay their costs over multiple turns.
    When a player leaves cycles unused, they go toward paying the cycle costs of threaded functions
    Each player can own a maximum of two threads.

* Cards
    You start the game with five cards.
    At the beginning of your turn, you draw one card.
    Each player can have a maximum of eight cards.

