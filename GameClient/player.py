class Player:
    def __init__(self):
        self.move = None
        self.send = False

    def play(self):
        temp = self.move
        self.move = None
        if temp is None:
            return temp
        return temp

    def playAI(self):
        if not self.send:
            self.send = True
            return True
        temp = self.move
        self.move = None
        if temp is None:
            return temp
        self.send = False
        return temp
