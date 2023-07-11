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
                    pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE + x * GRID_SIZE,
                                                          self.y * GRID_SIZE + y * GRID_SIZE,
                                                          GRID_SIZE, GRID_SIZE))

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

# ゲームの初期化
def init_game():
    grid = [[None] * GRID_WIDTH for i in range(GRID_HEIGHT)]
    tetrimino = Tetrimino()
    game_over = False
    return grid, tetrimino, game_over

# ゲームのメインループ
def run_game():
    grid, tetrimino, game_over = init_game()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrimino.move(-1, 0)
                    if tetrimino.collides(grid):
                        tetrimino.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetrimino.move(1, 0)
                    if tetrimino.collides(grid):
                        tetrimino.move(-1, 0)
        tetrimino.move(0, 1)
        if tetrimino.collides(grid):
            tetrimino.move(0, -1)
            tetrimino.place(grid)
            tetrimino = Tetrimino()
            if tetrimino.collides(grid):
                game_over = True

        screen.fill((0, 0, 0))
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(screen, col, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        tetrimino.draw()
        pygame.display.flip()
        clock.tick(30)

    # フォントの初期化
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)

    text = font.render("GameOver", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

    pygame.quit()

# ゲームの実行
run_game()