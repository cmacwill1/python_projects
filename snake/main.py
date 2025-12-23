import random

class Food:
    def __init__(self):
        self.pos_x = random.randint(0,10)
        self.pos_y = random.randint(0,10)


class Snake:
    def __init__(self):
        self.maxlen = 1
        self.pos_x = [10]
        self.pos_y = [10]
        self.direction = "up"
        self.grow = False

    def eat(self):
        self.maxlen += 1

    def move(self):
        if self.direction == "up":
            self.pos_x.append(self.pos_x[-1])
            self.pos_y.append(self.pos_y[-1] - 1)
        if self.direction == "down":
            self.pos_x.append(self.pos_x[-1])
            self.pos_y.append(self.pos_y[-1] + 1)
        if self.direction == "left":
            self.pos_x.append(self.pos_x[-1] - 1)
            self.pos_y.append(self.pos_y[-1])
        if self.direction == "right":
            self.pos_x.append(self.pos_x[-1] + 1)
            self.pos_y.append(self.pos_y[-1])

    def tail_pop(self):
        if self.grow == True:
            pass
        else:
            self.pos_x.pop(0)
            self.pos_y.pop(0)
