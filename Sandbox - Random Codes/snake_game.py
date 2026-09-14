import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

BLACK = (20, 20, 20)
GREEN = (0, 200, 80)
DARK_GREEN = (0, 140, 60)
RED = (220, 60, 60)
WHITE = (240, 240, 240)
GRAY = (60, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 40, bold=True)


def random_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def game_loop():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_direction = (1, 0)
    food = random_food(snake)
    score = 0
    speed = 8
    paused = False

    while True:
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
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        if paused:
            screen.fill(BLACK)
            draw_grid()
            pause_text = big_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 20))
            pygame.display.flip()
            clock.tick(10)
            continue

        direction = next_direction
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
            return score
        if new_head in snake:
            return score

        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            food = random_food(snake)
            if speed < 20 and score % 50 == 0:
                speed += 1
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid()

        fx, fy = food
        pygame.draw.rect(screen, RED, (fx * CELL + 2, fy * CELL + 2, CELL - 4, CELL - 4))

        for i, (sx, sy) in enumerate(snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (sx * CELL + 1, sy * CELL + 1, CELL - 2, CELL - 2))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 8))

        pygame.display.flip()
        clock.tick(speed)


def main():
    while True:
        final_score = game_loop()

        screen.fill(BLACK)
        over = big_font.render("GAME OVER", True, RED)
        score_display = font.render(f"Final Score: {final_score}", True, WHITE)
        restart = font.render("Press R to restart, Q to quit", True, WHITE)

        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 70))
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    main()