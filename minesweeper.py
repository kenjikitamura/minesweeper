import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Test", fps=60)
        pyxel.mouse(True)
        self.pos = Vec2(0,0)
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
        #pyxel.blt(61, 66, 0,0,0,38,16)

App()
        