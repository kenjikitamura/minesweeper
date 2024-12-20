import pyxel
import random

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256


def draw_text_with_border(x, y, s, col, bcol, font):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                pyxel.text(
                    x + dx,
                    y + dy,
                    s,
                    bcol,
                    font,
                )
    pyxel.text(x, y, s, col, font)

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
    
    def update(self):
        self.size += 1

    def draw(self):
        pyxel.circ(self.x, self.y, self.size, 8)

class Cell:
    TYPE_EMPTY = 0 # 空欄
    TYPE_BOMB = 1 # 爆弾
    TYPE_WALL = 2 # 周囲の壁(番兵)
    STATUS_OPEN = 0 # 開いた状態
    STATUS_CLOSE = 1 # 開いていない状態
    STATUS_CHECK = 2 # 開いておらず、爆弾があるとチェックした状態

    def __init__(self):
        self.type = Cell.TYPE_EMPTY
        self.status = Cell.STATUS_CLOSE
class Board:
    def __init__(self, width, height):
        self.size_w = width + 2 # 番兵で+2
        self.size_h = height + 2 # 番兵で+2
        self.start_x = 5
        self.start_y = 20
        self.grid = [[Cell() for _ in range(self.size_w)] for _ in range(self.size_h)]
        self.bomb = Bomb(0, 0)

        # 壁を設定
        for y in range(self.size_h):
            self.grid[y][0].type = Cell.TYPE_WALL
            self.grid[y][width+1].type = Cell.TYPE_WALL
        for x in range(self.size_w):
            self.grid[0][x].type = Cell.TYPE_WALL
            self.grid[height+1][x].type = Cell.TYPE_WALL

        # 爆弾を設定
        self.bombSize = 20

        # 爆弾が設置していないところに爆弾を設置する
        for i in range(self.bombSize):
            while True:
                x = random.randrange(0,width)+1
                y = random.randrange(0,height)+1
                if self.grid[y][x].type == Cell.TYPE_EMPTY:
                    self.grid[y][x].type = Cell.TYPE_BOMB
                    break

    def draw(self):
        flags = 0
        for y, raw in enumerate(self.grid):
            for x, item in enumerate(raw):
                # 壁を描画
                if item.type == Cell.TYPE_WALL:
                    pyxel.blt(x*16 + self.start_x, y*16 + self.start_y ,0, 0,16,16,16)

                # 爆弾チェックを描画
                elif item.status == Cell.STATUS_CHECK:
                    pyxel.blt(x*16 + self.start_x, y*16 + self.start_y ,0, 48,0,16,16)
                    flags += 1

                # 空けてないマスを描画
                elif item.status == Cell.STATUS_CLOSE:
                    pyxel.blt(x*16 + self.start_x, y*16 + self.start_y ,0, 0,0,16,16)

                # 空けているマスを描画
                else:
                    if item.type == Cell.TYPE_EMPTY:
                        pyxel.blt(x*16 + self.start_x, y*16 + self.start_y, 0, 16,0,16,16)
                        bombCount = self.bombCount(x,y)
                        if bombCount > 0:
                            pyxel.text(x*16 + 5 + self.start_x, y*16 + 5 + self.start_y, f"{bombCount}", 4)
                    elif item.type == Cell.TYPE_BOMB:
                        pyxel.blt(x*16 + self.start_x, y*16 + self.start_y, 0, 32,0,16,16)

        # ゲームオーバー時の爆発描画
        if self.bomb is not None:
            self.bomb.draw()

    # クリアしたかチェック
    # クリア = 爆弾以外を開いている かつ、全ての爆弾をチェックしている
    def checkClear(self):
        isAllOpen = True
        isAllCheck = True

        for iy in range(1, self.size_h):
            for ix in range(1, self.size_w):
                cell = self.grid[iy][ix]

                # 空欄を全て開いているか
                if cell.type == Cell.TYPE_EMPTY and cell.status != Cell.STATUS_OPEN:
                    isAllOpen = False

                # 爆弾をチェックしているか
                if cell.type == Cell.TYPE_BOMB and cell.status != Cell.STATUS_CHECK:
                    isAllCheck = False
        # print(f"isAllCheck={isAllCheck}, isAllOpen={isAllOpen}")
        return isAllCheck and isAllOpen


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
        click_x = (x - self.start_x)//16
        click_y = (y - self.start_y)//16
        if click_x >= self.size_w or click_y >= self.size_h:
            return
        if self.grid[click_y][click_x].type == Cell.TYPE_WALL:
            return
        self.openCell(click_x, click_y)
            
        pyxel.play(0, 0) # beep音

        # 開いたのが爆弾だったらゲームオーバー
        if self.grid[click_y][click_x].type == Cell.TYPE_BOMB:
            self.bomb = Bomb(x, y)
            return False
        else:
            return True

    def onRightClick(self, x, y):
        click_x = (x - self.start_x)//16
        click_y = (y - self.start_y)//16
        if click_x >= self.size_w or click_y >= self.size_h:
            return
        if self.grid[click_y][click_x].type == Cell.TYPE_WALL:
            return
        if self.grid[click_y][click_x].status == Cell.STATUS_OPEN:
            return
        if self.grid[click_y][click_x].status == Cell.STATUS_CLOSE:
            self.grid[click_y][click_x].status = Cell.STATUS_CHECK
        else:
            self.grid[click_y][click_x].status = Cell.STATUS_CLOSE

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
    SCENE_TITLE = 0
    SCENE_INGAME = 1
    SCENE_GAME_OVER = 2
    SCENE_CLEAR = 3
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Mine Sweeper", fps=60)
        pyxel.load("data.pyxres")
        pyxel.mouse(True)
        self.reset()
        self.umplus10 = pyxel.Font("assets/umplus_j10r.bdf")
        self.umplus12 = pyxel.Font("assets/umplus_j12r.bdf")
        self.title_image = pyxel.Image.from_image(filename="assets/title3.png")
        self.scene_change_wait = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # タイトル画面
        if self.scene == App.SCENE_TITLE:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE) and self.scene_change_wait < 0:
                self.scene = App.SCENE_INGAME
                self.scene_change_wait = 30

        # ゲーム中
        if self.scene == App.SCENE_INGAME:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.scene_change_wait < 0:
                flag = self.board.onClick(pyxel.mouse_x, pyxel.mouse_y)
                if flag is False:
                    self.scene = App.SCENE_GAME_OVER
                    self.scene_change_wait = 30

            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.scene_change_wait < 0:
                self.board.onRightClick(pyxel.mouse_x, pyxel.mouse_y)
            if self.board.checkClear():
                self.scene = App.SCENE_CLEAR
                self.scene_change_wait = 30

        # ゲームオーバー
        if self.scene == App.SCENE_GAME_OVER and self.board.bomb is not None:
            self.board.bomb.update()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.scene_change_wait < 0:
                self.reset()
        
        self.scene_change_wait -= 1
        
    def draw(self):
        pyxel.cls(0)

        # タイトル画面
        if self.scene == App.SCENE_TITLE:
            pyxel.blt(x=10, y=20, img=self.title_image, u=0, v=0, w= 230, h=110, colkey=0)
            draw_text_with_border(90,150, "Push Space Key", 7, 5, self.umplus12)

        # ゲーム中
        if self.scene == App.SCENE_INGAME:
            self.board.draw()

        # ゲームオーバー
        if self.scene == App.SCENE_GAME_OVER:
            self.board.draw()
            draw_text_with_border(90,5, "Game Over!!", 7, 5, self.umplus12)

        # ゲームクリア
        if self.scene == App.SCENE_CLEAR:
            draw_text_with_border(90,5, "Game Clear!!", 7, 5, self.umplus12)
            self.board.draw()

        # 説明表示
        if self.scene == App.SCENE_INGAME:
            draw_text_with_border(5,5, "左クリックでマスを開く 右クリックで爆弾をマーク", 7, 5, self.umplus10)

    # ゲーム開始またはゲームオーバー後のリセット
    def reset(self):
        self.board = Board(13,12)
        self.scene = self.SCENE_TITLE
        self.scene_change_wait = 30
        
App()
        