import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:
    TYPE_EMPTY = 0
    TYPE_BOMB = 1

    def __init__(self):
        self.type = Cell.TYPE_EMPTY
class Board:
    def __init__(self, width, height):
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def draw(self):
        for y, raw in enumerate(self.grid):
            for x, item in enumerate(raw):
                pyxel.text(x*10, y*10, "O", 5)
class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Test", fps=60)
        pyxel.mouse(True)
        self.pos = Vec2(0,0)
        self.board = Board(10,10)
        pyxel.run(self.update, self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.pos.x = pyxel.mouse_x
            self.pos.y = pyxel.mouse_y

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55,41,"Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.text(self.pos.x, self.pos.y, "HERE!", 5)
        self.board.draw()
App()
        