import pygame
import random

# ゲーム画面の設定
WIDTH, HEIGHT = 400, 650
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# テトリスのブロックの定義
tetriminos = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

# テトリスのブロックを表すクラス
class Tetrimino:
    def __init__(self):
        self.shape = random.choice(tetriminos)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, col in enumerate(row):
                if col:
                    rect = pygame.Rect((self.x + x) * GRID_SIZE,(self.y + y) * GRID_SIZE,GRID_SIZE,GRID_SIZE)
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)#ブロックが落下する前にブロックの中の四角一つに外枠を描画

    def collides(self, grid):
        for y, row in enumerate(self.shape):
            for x, col in enumerate(row):
                if col and (self.y + y >= GRID_HEIGHT or self.x + x < 0 or self.x + x >= GRID_WIDTH or
                            grid[self.y + y][self.x + x]):
                    return True
        return False

    def place(self, grid):
        for y, row in enumerate(self.shape):
            for x, col in enumerate(row):
                if col:
                    grid[self.y + y][self.x + x] = self.color

    def drop_to_bottom(self, grid):
        while not self.collides(grid):#他のブロックに衝突しなければループ
            self.move(0, 1)
        self.move(0, -1)
        self.place(grid)
        return Tetrimino()

# ゲームの初期化
def init_game():
    grid = [[None] * GRID_WIDTH for i in range(GRID_HEIGHT)]
    tetrimino = Tetrimino()
    game_over = False

def init_game():
    grid = [[None] * GRID_WIDTH for i in range(GRID_HEIGHT)]
    tetrimino = Tetrimino()
    game_over = False
    return grid, tetrimino, game_over    

# 行が揃っているかをチェックし、揃っている行を削除する
def check_lines(grid):
    full_rows = []
    for y, row in enumerate(grid):
        if all(row):
            full_rows.append(y)

    for row_index in full_rows:
        del grid[row_index]
        grid.insert(0, [None] * GRID_WIDTH)

# ゲームのメインループ
def run_game():
    grid, tetrimino, game_over = init_game()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrimino.move(-1, 0)
                    if tetrimino.collides(grid):
                        tetrimino.move(1, 0)

                elif event.key == pygame.K_RIGHT:
                    tetrimino.move(1, 0)
                    if tetrimino.collides(grid):
                        tetrimino.move(-1, 0)

                elif event.key == pygame.K_SPACE:
                    tetrimino.rotate()
                    if tetrimino.collides(grid):
                        tetrimino.rotate()
            
                elif event.key == pygame.K_DOWN:#DOWNキーが押されれば
                    tetrimino.drop_to_bottom(grid)

        tetrimino.move(0, 1)
        if tetrimino.collides(grid):
            tetrimino.move(0, -1)
            tetrimino.place(grid)
            check_lines(grid)
            tetrimino = Tetrimino()
            if tetrimino.collides(grid):
                game_over = True

        screen.fill((0, 0, 0))
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if col:
                    rect = pygame.Rect(
                        x * GRID_SIZE,
                        y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )
                    pygame.draw.rect(screen, col, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1) #ブロック落下後にブロックの中の四角一つに外枠を描画

        tetrimino.draw()
        pygame.display.flip()
        clock.tick(5)

# ゲームの実行
run_game()