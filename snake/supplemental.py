import numpy as np

class Food:
    def __init__(self, x, y):
        self.pos = np.array([x,y])

class Snake:
    def __init__(self, map_size):
        self.maxlen = 1
        self.pos = np.array([[int(round(map_size/2)),int(round(map_size/2))]])
        self.direction = "up"
        self.grow = False

    def move(self):
        if self.direction == "up":
            self.pos = np.append(self.pos, np.array([[self.pos[-1][0],self.pos[-1][1] - 1]]), axis=0)
        if self.direction == "down":
            self.pos = np.append(self.pos, np.array([[self.pos[-1][0],self.pos[-1][1] + 1]]), axis=0)
        if self.direction == "left":
            self.pos = np.append(self.pos, np.array([[self.pos[-1][0] - 1,self.pos[-1][1]]]), axis=0)
        if self.direction == "right":
            self.pos = np.append(self.pos, np.array([[self.pos[-1][0] + 1,self.pos[-1][1]]]), axis=0)

    def tail_pop(self):
        if self.grow == True:
            pass
        else:
            self.pos = np.delete(self.pos, 0, axis=0)
