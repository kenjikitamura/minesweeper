import pyxel
import random

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:
    TYPE_EMPTY = 0
    TYPE_BOMB = 1
    TYPE_WALL = 2
    STATUS_OPEN = 0
    STATUS_CLOSE = 1

    def __init__(self):
        self.type = Cell.TYPE_EMPTY
        self.status = Cell.STATUS_CLOSE
class Board:
    def __init__(self, width, height):
        self.size_w = width + 2 # 番兵で+2
        self.size_h = height + 2 # 番兵で+2
        self.grid = [[Cell() for _ in range(self.size_w)] for _ in range(self.size_h)]

        # 壁を設定
        for y in range(self.size_h):
            self.grid[0][y].type = Cell.TYPE_WALL
            self.grid[width+1][y].type = Cell.TYPE_WALL
        for x in range(self.size_w):
            self.grid[x][0].type = Cell.TYPE_WALL
            self.grid[x][height+1].type = Cell.TYPE_WALL

        # 爆弾を設定
        BOMB_SIZE = 10
        for i in range(BOMB_SIZE):
            self.grid[random.randrange(0,width)+1][random.randrange(0,height)+1].type = Cell.TYPE_BOMB

    def draw(self):
        for y, raw in enumerate(self.grid):
            for x, item in enumerate(raw):
                # 壁を描画
                if item.type == Cell.TYPE_WALL:
                    pyxel.blt(x*16,y*16,0, 48,0,16,16)

                # 空けてないマスを描画
                elif item.status == Cell.STATUS_CLOSE:
                    pyxel.blt(x*16,y*16,0, 0,0,16,16)

                # 空けているマスを描画
                else:
                    if item.type == Cell.TYPE_EMPTY:
                        pyxel.blt(x*16,y*16,0, 16,0,16,16)
                        bombCount = self.bombCount(x,y)
                        if bombCount > 0:
                            pyxel.text(x*16 + 5, y*16 + 5, f"{bombCount}", 4)
                    elif item.type == Cell.TYPE_BOMB:
                        pyxel.blt(x*16,y*16,0, 32,0,16,16)

    # x,y座標の周りの爆弾の数を取得する
    def bombCount(self, x, y):
        count = 0
        for iy in range(y-1, y+2):
            for ix in range(x-1, x+2):
                if ix == x and iy == y:
                    continue
                if self.grid[iy][ix].type == Cell.TYPE_BOMB:
                    count += 1
        return count

    # ボードのクリック処理を実行
    def onClick(self, x, y):
        click_x = x//16
        click_y = y//16
        if click_x >= self.size_w or click_y >= self.size_h:
            return
        if self.grid[click_y][click_x].type == Cell.TYPE_WALL:
            return
        self.openCell(click_x, click_y)

    # マスを開く処理
    def openCell(self, x, y):
        self.grid[y][x].status = Cell.STATUS_OPEN
        bombCount = self.bombCount(x, y)
        if bombCount == 0 and self.grid[y][x].type == Cell.TYPE_EMPTY:
            self.openCells(x, y)

    # 周りのマスを全部開く
    def openCells(self, x, y):
        for iy in range(y-1, y+2):
            for ix in range(x-1, x+2):
                if self.grid[iy][ix].status == Cell.STATUS_CLOSE and self.grid[iy][ix].type == Cell.TYPE_EMPTY:
                    self.openCell(ix, iy)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Test", fps=60)
        pyxel.load("data.pyxres")
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
            self.board.onClick(pyxel.mouse_x, pyxel.mouse_y)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55,41,"Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.text(self.pos.x, self.pos.y, "HERE!", 5)
        self.board.draw()
        
App()
        