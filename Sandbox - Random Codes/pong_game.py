import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 500
WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GRAY = (80, 80, 80)
BLUE = (70, 130, 200)
ORANGE = (230, 140, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 30)
big_font = pygame.font.SysFont("consolas", 60, bold=True)

PADDLE_W = 12
PADDLE_H = 90
PADDLE_SPEED = 7

BALL_SIZE = 14
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

WIN_SCORE = 7


def reset_ball(direction=1):
    return {
        "x": WIDTH // 2 - BALL_SIZE // 2,
        "y": HEIGHT // 2 - BALL_SIZE // 2,
        "vx": BALL_SPEED_X * direction,
        "vy": BALL_SPEED_Y * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
    }


def show_message(text, sub_text=""):
    screen.fill(BLACK)
    msg = big_font.render(text, True, WHITE)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
    if sub_text:
        sub = font.render(sub_text, True, GRAY)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()


def main():
    left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
    right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)

    left_score = 0
    right_score = 0
    ball = reset_ball()

    running = True

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED

        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]

        if ball["y"] <= 0 or ball["y"] + BALL_SIZE >= HEIGHT:
            ball["vy"] *= -1
            ball["y"] = max(0, min(HEIGHT - BALL_SIZE, ball["y"]))

        ball_rect = pygame.Rect(ball["x"], ball["y"], BALL_SIZE, BALL_SIZE)

        if ball_rect.colliderect(left_paddle) and ball["vx"] < 0:
            ball["vx"] *= -1
            offset = (ball_rect.centery - left_paddle.centery) / (PADDLE_H / 2)
            ball["vy"] += offset * 2
            ball["x"] = left_paddle.right

        if ball_rect.colliderect(right_paddle) and ball["vx"] > 0:
            ball["vx"] *= -1
            offset = (ball_rect.centery - right_paddle.centery) / (PADDLE_H / 2)
            ball["vy"] += offset * 2
            ball["x"] = right_paddle.left - BALL_SIZE

        ball["vy"] = max(-9, min(9, ball["vy"]))

        if ball["x"] < -BALL_SIZE:
            right_score += 1
            ball = reset_ball(direction=1)
        elif ball["x"] > WIDTH + BALL_SIZE:
            left_score += 1
            ball = reset_ball(direction=-1)

        if left_score >= WIN_SCORE or right_score >= WIN_SCORE:
            winner = "PLAYER 1 WINS" if left_score >= WIN_SCORE else "PLAYER 2 WINS"
            show_message(winner, "Press R to play again, Q to quit")
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
            left_score = 0
            right_score = 0
            ball = reset_ball()
            left_paddle.centery = HEIGHT // 2
            right_paddle.centery = HEIGHT // 2

        screen.fill(BLACK)

        for y in range(0, HEIGHT, 30):
            pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 15))

        pygame.draw.rect(screen, BLUE, left_paddle)
        pygame.draw.rect(screen, ORANGE, right_paddle)

        pygame.draw.rect(screen, WHITE, (ball["x"], ball["y"], BALL_SIZE, BALL_SIZE))

        left_text = font.render(str(left_score), True, BLUE)
        right_text = font.render(str(right_score), True, ORANGE)
        screen.blit(left_text, (WIDTH // 2 - 70, 20))
        screen.blit(right_text, (WIDTH // 2 + 50, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()