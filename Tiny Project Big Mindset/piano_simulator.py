import pygame
import numpy as np
import sys

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

SAMPLE_RATE = 44100

WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
BLACK_KEYS_MAP = {
    'C': 'C#', 'D': 'D#', 'F': 'F#', 'G': 'G#', 'A': 'A#'
}

KEY_FREQS = {
    'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
    'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
    'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
}

KEYBOARD_MAP = {
    pygame.K_a: 'C', pygame.K_w: 'C#', pygame.K_s: 'D',
    pygame.K_e: 'D#', pygame.K_d: 'E', pygame.K_f: 'F',
    pygame.K_t: 'F#', pygame.K_g: 'G', pygame.K_y: 'G#',
    pygame.K_h: 'A', pygame.K_u: 'A#', pygame.K_j: 'B',
    pygame.K_k: 'C5', pygame.K_o: 'C#5', pygame.K_l: 'D5',
    pygame.K_p: 'D#5', pygame.K_SEMICOLON: 'E5'
}

OCTAVE_FREQS = {
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25
}


def generate_tone(freq, duration=1.5, volume=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(freq * t * 2 * np.pi)

    # add harmonics for piano-ish tone
    wave += 0.5 * np.sin(freq * 2 * t * 2 * np.pi)
    wave += 0.25 * np.sin(freq * 3 * t * 2 * np.pi)
    wave += 0.125 * np.sin(freq * 4 * t * 2 * np.pi)

    # ADSR envelope
    attack = int(0.01 * SAMPLE_RATE)
    decay = int(0.1 * SAMPLE_RATE)
    sustain = int(0.5 * SAMPLE_RATE)
    release = int(0.9 * SAMPLE_RATE)

    envelope = np.ones(len(t))
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[attack:attack+decay] = np.linspace(1, 0.7, decay)
    envelope[attack+decay:attack+decay+sustain] = 0.7
    end_idx = attack + decay + sustain + release
    if end_idx < len(envelope):
        envelope[attack+decay+sustain:end_idx] = np.linspace(0.7, 0, release)
        envelope[end_idx:] = 0

    wave *= envelope * volume
    stereo = np.column_stack((wave, wave))
    return (stereo * 32767).astype(np.int16)


# Pre-generate sounds
SOUNDS = {}
for note, freq in {**KEY_FREQS, **OCTAVE_FREQS}.items():
    SOUNDS[note] = pygame.sndarray.make_sound(generate_tone(freq))


WIDTH = 900
HEIGHT = 400
WHITE_KEY_W = WIDTH // 8
WHITE_KEY_H = HEIGHT
BLACK_KEY_W = WHITE_KEY_W // 2
BLACK_KEY_H = HEIGHT * 2 // 3

WHITE = (250, 250, 250)
BLACK = (25, 25, 25)
PRESSED_WHITE = (180, 220, 255)
PRESSED_BLACK = (70, 90, 130)
TEXT_COLOR = (60, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)
info_font = pygame.font.SysFont("consolas", 13)

key_labels = ['A', 'W', 'S', 'E', 'D', 'F', 'T', 'G', 'Y', 'H', 'U', 'J', 'K', 'O', 'L', 'P', ';']

active_keys = set()

channels = {}

def play_note(note):
    if note in SOUNDS:
        channel = SOUNDS[note].play()
        if channel:
            channels[note] = channel
        return channel
    return None


def stop_note(note):
    if note in channels:
        channels[note].stop()
        del channels[note]


def get_white_key_rect(index):
    return pygame.Rect(index * WHITE_KEY_W, 0, WHITE_KEY_W, WHITE_KEY_H)


def get_black_key_positions():
    positions = []
    for i in range(7):
        white_note = WHITE_KEYS[i]
        if white_note in BLACK_KEYS_MAP:
            x = (i + 1) * WHITE_KEY_W - BLACK_KEY_W // 2
            positions.append((BLACK_KEYS_MAP[white_note], x))
    return positions


BLACK_POSITIONS = get_black_key_positions()


def draw_piano():
    screen.fill((230, 230, 230))

    for i, note in enumerate(WHITE_KEYS):
        rect = get_white_key_rect(i)
        color = PRESSED_WHITE if note in active_keys else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        label = font.render(note, True, TEXT_COLOR)
        screen.blit(label, (rect.centerx - label.get_width() // 2, HEIGHT - 40))

    for note, x in BLACK_POSITIONS:
        rect = pygame.Rect(x, 0, BLACK_KEY_W, BLACK_KEY_H)
        color = PRESSED_BLACK if note in active_keys else BLACK
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        label = font.render(note, True, (220, 220, 220))
        screen.blit(label, (rect.centerx - label.get_width() // 2, BLACK_KEY_H - 25))

    hint = info_font.render("A W S E D F T G Y H U J  |  K O L P ;  |  ESC to quit", True, TEXT_COLOR)
    screen.blit(hint, (10, 10))


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in KEYBOARD_MAP:
                    note = KEYBOARD_MAP[event.key]
                    if note not in active_keys:
                        active_keys.add(note)
                        play_note(note)
            if event.type == pygame.KEYUP:
                if event.key in KEYBOARD_MAP:
                    note = KEYBOARD_MAP[event.key]
                    if note in active_keys:
                        active_keys.discard(note)

        draw_piano()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()