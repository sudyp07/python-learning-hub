import pygame
import random
import sys

pygame.init()

CELL = 30
COLS = 10
ROWS = 20
PLAY_W = COLS * CELL
PLAY_H = ROWS * CELL
SIDE_W = 200
WIDTH = PLAY_W + SIDE_W
HEIGHT = PLAY_H

BLACK = (12, 12, 18)
GRID = (35, 35, 45)
WHITE = (240, 240, 240)
GRAY = (90, 90, 100)

COLORS = {
    "I": (0, 200, 220),
    "O": (230, 200, 40),
    "T": (170, 70, 200),
    "S": (60, 200, 90),
    "Z": (220, 60, 60),
    "J": (60, 100, 220),
    "L": (230, 140, 50),
}

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)
big_font = pygame.font.SysFont("consolas", 34, bold=True)


class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.shape = [row[:] for row in SHAPES[kind]]
        self.color = COLORS[kind]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def cells(self, ox=0, oy=0, shape=None):
        s = shape if shape else self.shape
        result = []
        for r, row in enumerate(s):
            for c, val in enumerate(row):
                if val:
                    result.append((self.x + c + ox, self.y + r + oy))
        return result

    def rotate(self):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        return rotated


def new_board():
    return [[None for _ in range(COLS)] for _ in range(ROWS)]


def valid(board, cells):
    for x, y in cells:
        if x < 0 or x >= COLS or y >= ROWS:
            return False
        if y >= 0 and board[y][x]:
            return False
    return True


def lock_piece(board, piece):
    for x, y in piece.cells():
        if 0 <= y < ROWS and 0 <= x < COLS:
            board[y][x] = piece.color


def clear_lines(board):
    new_rows = [row for row in board if not all(row)]
    cleared = ROWS - len(new_rows)
    for _ in range(cleared):
        new_rows.insert(0, [None for _ in range(COLS)])
    return new_rows, cleared


def draw_block(x, y, color, offset_x=0):
    rect = pygame.Rect(offset_x + x * CELL, y * CELL, CELL, CELL)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)


def draw_board(board, offset_x=0):
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(offset_x + x * CELL, y * CELL, CELL, CELL)
            pygame.draw.rect(screen, GRID, rect, 1)
            if board[y][x]:
                draw_block(x, y, board[y][x], offset_x)


def draw_piece(piece, offset_x=0, ghost=False, ghost_y=None):
    color = piece.color
    if ghost:
        color = (50, 50, 60)

    if ghost_y is not None:
        old_y = piece.y
        piece.y = ghost_y
        cells = piece.cells()
        piece.y = old_y
    else:
        cells = piece.cells()

    for x, y in cells:
        if y >= 0:
            draw_block(x, y, color, offset_x)


def draw_side(score, level, lines, next_piece):
    x_offset = PLAY_W
    pygame.draw.rect(screen, BLACK, (x_offset, 0, SIDE_W, HEIGHT))
    pygame.draw.line(screen, GRAY, (x_offset, 0), (x_offset, HEIGHT), 2)

    title = big_font.render("TETRIS", True, WHITE)
    screen.blit(title, (x_offset + 20, 15))

    score_lbl = font.render("SCORE", True, GRAY)
    score_val = font.render(str(score), True, WHITE)
    screen.blit(score_lbl, (x_offset + 20, 80))
    screen.blit(score_val, (x_offset + 20, 105))

    level_lbl = font.render("LEVEL", True, GRAY)
    level_val = font.render(str(level), True, WHITE)
    screen.blit(level_lbl, (x_offset + 20, 150))
    screen.blit(level_val, (x_offset + 20, 175))

    lines_lbl = font.render("LINES", True, GRAY)
    lines_val = font.render(str(lines), True, WHITE)
    screen.blit(lines_lbl, (x_offset + 20, 220))
    screen.blit(lines_val, (x_offset + 20, 245))

    next_lbl = font.render("NEXT", True, GRAY)
    screen.blit(next_lbl, (x_offset + 20, 300))

    if next_piece:
        shape = SHAPES[next_piece]
        color = COLORS[next_piece]
        box_x = x_offset + 20
        box_y = 330
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(box_x + c * CELL, box_y + r * CELL, CELL, CELL)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)

    help1 = font.render("Arrows: move", True, GRAY)
    help2 = font.render("Up: rotate", True, GRAY)
    help3 = font.render("Space: drop", True, GRAY)
    help4 = font.render("P: pause", True, GRAY)
    help5 = font.render("Esc: quit", True, GRAY)

    screen.blit(help1, (x_offset + 20, 460))
    screen.blit(help2, (x_offset + 20, 485))
    screen.blit(help3, (x_offset + 20, 510))
    screen.blit(help4, (x_offset + 20, 535))
    screen.blit(help5, (x_offset + 20, 560))


def game_over_screen(score):
    overlay = pygame.Surface((PLAY_W, PLAY_H))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    msg = big_font.render("GAME OVER", True, (220, 60, 60))
    screen.blit(msg, (PLAY_W // 2 - msg.get_width() // 2, PLAY_H // 2 - 60))

    sc = font.render(f"Score: {score}", True, WHITE)
    screen.blit(sc, (PLAY_W // 2 - sc.get_width() // 2, PLAY_H // 2))

    hint = font.render("R: restart   Q: quit", True, GRAY)
    screen.blit(hint, (PLAY_W // 2 - hint.get_width() // 2, PLAY_H // 2 + 50))
    pygame.display.flip()


def new_piece():
    return Piece(random.choice(list(SHAPES.keys())))


def main():
    board = new_board()
    current = new_piece()
    next_kind = random.choice(list(SHAPES.keys()))
    score = 0
    lines = 0
    level = 1

    fall_time = 0
    fall_speed = 500

    paused = False

    while True:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_p:
                    paused = not paused

                if paused:
                    continue

                if event.key == pygame.K_LEFT:
                    if valid(board, current.cells(-1, 0)):
                        current.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if valid(board, current.cells(1, 0)):
                        current.x += 1
                elif event.key == pygame.K_DOWN:
                    if valid(board, current.cells(0, 1)):
                        current.y += 1
                elif event.key == pygame.K_UP:
                    rotated = current.rotate()
                    if valid(board, current.cells(shape=rotated)):
                        current.shape = rotated
                elif event.key == pygame.K_SPACE:
                    while valid(board, current.cells(0, 1)):
                        current.y += 1

        if paused:
            screen.fill(BLACK)
            draw_board(board)
            draw_piece(current)
            draw_side(score, level, lines, next_kind)
            pause_text = big_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (PLAY_W // 2 - pause_text.get_width() // 2, PLAY_H // 2))
            pygame.display.flip()
            continue

        if fall_time >= fall_speed:
            fall_time = 0
            if valid(board, current.cells(0, 1)):
                current.y += 1
            else:
                lock_piece(board, current)
                board, cleared = clear_lines(board)
                if cleared:
                    lines += cleared
                    score += [0, 100, 300, 500, 800][cleared] * level
                    level = lines // 10 + 1
                    fall_speed = max(80, 500 - (level - 1) * 40)

                current = Piece(next_kind)
                next_kind = random.choice(list(SHAPES.keys()))

                if not valid(board, current.cells()):
                    game_over_screen(score)
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
                                if event.key == pygame.K_r:
                                    waiting = False

                    board = new_board()
                    current = new_piece()
                    next_kind = random.choice(list(SHAPES.keys()))
                    score = 0
                    lines = 0
                    level = 1
                    fall_speed = 500
                    fall_time = 0

        screen.fill(BLACK)

        ghost_y = current.y
        while valid(board, current.cells(0, ghost_y - current.y + 1)):
            ghost_y += 1

        draw_board(board)
        draw_piece(current, ghost=True, ghost_y=ghost_y)
        draw_piece(current)
        draw_side(score, level, lines, next_kind)

        pygame.draw.line(screen, GRAY, (PLAY_W, 0), (PLAY_W, HEIGHT), 2)

        pygame.display.flip()


if __name__ == "__main__":
    main()