from enum import Enum

BLOCK_SIZE = 2 ** 14


class State(Enum):  
    Free,Pending,Full = range(1,3)


class Block():
    def __init__(self, state = State.FREE, block_size = BLOCK_SIZE, data = b'', last_seen = 0):
        self.state = state
        self.block_size = block_size
        self.data = data
        self.last_seen = last_seen

    def __str__(self):
        return "%s - %d - %d - %d" % (self.state, self.block_size, len(self.data), self.last_seen)