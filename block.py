from enum import Enum

BLOCK_SIZE = 2 ** 14


class State(Enum):  
    FREE,PEDNING,FULL = range(0,3)


class Block():
    def __init__(self, state = State.FREE, block_size = BLOCK_SIZE, data = b'', last_seen = 0):
        self.state = state
        self.block_size = block_size
        self.data = data
        self.last_seen = last_seen
