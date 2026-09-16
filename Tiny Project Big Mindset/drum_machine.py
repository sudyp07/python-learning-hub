import pygame
import numpy as np
import sys

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

SAMPLE_RATE = 44100

# --- Drum synthesis ---

def kick():
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    freq = 150 * np.exp(-t * 20) + 40
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 8)
    wave *= envelope * 0.9
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


def snare():
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 15)
    noise = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 12)
    wave = tone * 0.5 + noise * 0.7
    wave *= 0.7
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


def hihat_closed():
    duration = 0.08
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    # high-pass by differencing
    noise = np.diff(noise, prepend=0)
    envelope = np.exp(-t * 60)
    wave = noise * envelope * 0.4
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


def hihat_open():
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    noise = np.diff(noise, prepend=0)
    envelope = np.exp(-t * 8)
    wave = noise * envelope * 0.35
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


def clap():
    duration = 0.35
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    # envelope with multiple bursts
    envelope = np.zeros_like(t)
    for start, amp in [(0, 1.0), (0.01, 0.8), (0.02, 0.6), (0.03, 0.4)]:
        idx = int(start * SAMPLE_RATE)
        seg = np.exp(-(t[idx:] - t[idx]) * 40) * amp
        envelope[idx:idx+len(seg)] += seg[:len(envelope)-idx]
    wave = noise * envelope * 0.5
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


def tom(freq=120):
    duration = 0.35
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    f = freq * np.exp(-t * 5) + freq * 0.5
    wave = np.sin(2 * np.pi * f * t)
    envelope = np.exp(-t * 9)
    wave *= envelope * 0.7
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


def rimshot():
    duration = 0.1
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(2 * np.pi * 400 * t) * np.exp(-t * 40)
    wave += np.random.uniform(-1, 1, len(t)) * np.exp(-t * 50) * 0.3
    wave *= 0.7
    return (np.column_stack((wave, wave)) * 32767).astype(np.int16)


DRUM_SOUNDS = {
    "Kick":  pygame.sndarray.make_sound(kick()),
    "Snare": pygame.sndarray.make_sound(snare()),
    "HiHat": pygame.sndarray.make_sound(hihat_closed()),
    "OpenHH": pygame.sndarray.make_sound(hihat_open()),
    "Clap":  pygame.sndarray.make_sound(clap()),
    "Tom":   pygame.sndarray.make_sound(tom()),
    "Rim":   pygame.sndarray.make_sound(rimshot()),
}

DRUM_KEYS = {
    pygame.K_q: "Kick",
    pygame.K_w: "Snare",
    pygame.K_e: "HiHat",
    pygame.K_r: "OpenHH",
    pygame.K_a: "Clap",
    pygame.K_s: "Tom",
    pygame.K_d: "Rim",
}

KEY_LABELS = {
    "Kick": "Q", "Snare": "W", "HiHat": "E", "OpenHH": "R",
    "Clap": "A", "Tom": "S", "Rim": "D"
}

# --- Grid sequencer ---

STEPS = 16
TRACKS = list(DRUM_SOUNDS.keys())

GRID = {track: [0] * STEPS for track in TRACKS}

WIDTH = 1000
HEIGHT = 500
CELL_W = 50
CELL_H = 50
LEFT_MARGIN = 130
TOP_MARGIN = 60

BG = (22, 24, 30)
GRID_LINE = (50, 54, 66)
BEAT_LINE = (90, 96, 120)
ACTIVE = (0, 200, 120)
ACTIVE_BEAT = (0, 230, 140)
CURSOR = (255, 200, 60)
TEXT = (230, 230, 235)
DIM = (140, 140, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drum Machine")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 15)
small = pygame.font.SysFont("consolas", 12)
title_font = pygame.font.SysFont("consolas", 20, bold=True)


def draw_grid(current_step, playing):
    screen.fill(BG)

    title = title_font.render("DRUM MACHINE", True, TEXT)
    screen.blit(title, (LEFT_MARGIN, 15))

    # Step numbers
    for s in range(STEPS):
        x = LEFT_MARGIN + s * CELL_W
        color = CURSOR if (playing and s == current_step) else DIM
        label = small.render(str(s + 1), True, color)
        screen.blit(label, (x + CELL_W // 2 - label.get_width() // 2, TOP_MARGIN - 22))

    # Track labels
    for i, track in enumerate(TRACKS):
        y = TOP_MARGIN + i * CELL_H
        label = font.render(track, True, TEXT)
        screen.blit(label, (15, y + CELL_H // 2 - label.get_height() // 2))

        key_hint = small.render(f"[{KEY_LABELS[track]}]", True, DIM)
        screen.blit(key_hint, (95, y + CELL_H // 2 - key_hint.get_height() // 2))

    # Grid cells
    for i, track in enumerate(TRACKS):
        for s in range(STEPS):
            x = LEFT_MARGIN + s * CELL_W
            y = TOP_MARGIN + i * CELL_H
            rect = pygame.Rect(x + 1, y + 1, CELL_W - 2, CELL_H - 2)

            is_active = GRID[track][s]

            if playing and s == current_step:
                base = CURSOR if not is_active else (255, 240, 100)
                pygame.draw.rect(screen, base, rect)
            elif is_active:
                color = ACTIVE_BEAT if s % 4 == 0 else ACTIVE
                pygame.draw.rect(screen, color, rect)
            else:
                pygame.draw.rect(screen, (35, 38, 48), rect)

            border_color = BEAT_LINE if s % 4 == 0 else GRID_LINE
            pygame.draw.rect(screen, border_color, rect, 1)

    # Help
    help_text = "Click cells to toggle | SPACE: play/stop | C: clear | Q-D keys: preview | ESC: quit"
    hint = small.render(help_text, True, DIM)
    screen.blit(hint, (LEFT_MARGIN, HEIGHT - 30))


def toggle_cell(mx, my):
    if mx < LEFT_MARGIN or my < TOP_MARGIN:
        return
    s = (mx - LEFT_MARGIN) // CELL_W
    i = (my - TOP_MARGIN) // CELL_H
    if 0 <= s < STEPS and 0 <= i < len(TRACKS):
        track = TRACKS[i]
        GRID[track][s] = 1 - GRID[track][s]


def main():
    playing = False
    current_step = 0
    bpm = 120
    step_duration = 60.0 / bpm / 4  # 16th notes

    last_step_time = pygame.time.get_ticks() / 1000.0
    preview_cooldown = {}

    running = True
    while running:
        now = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    playing = not playing
                    current_step = 0
                    last_step_time = now
                elif event.key == pygame.K_c:
                    for track in TRACKS:
                        GRID[track] = [0] * STEPS
                elif event.key == pygame.K_UP:
                    bpm = min(240, bpm + 5)
                    step_duration = 60.0 / bpm / 4
                elif event.key == pygame.K_DOWN:
                    bpm = max(40, bpm - 5)
                    step_duration = 60.0 / bpm / 4
                elif event.key in DRUM_KEYS:
                    DRUM_SOUNDS[DRUM_KEYS[event.key]].play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    toggle_cell(mx, my)

        if playing and (now - last_step_time) >= step_duration:
            last_step_time = now

            for track in TRACKS:
                if GRID[track][current_step]:
                    DRUM_SOUNDS[track].play()

            current_step = (current_step + 1) % STEPS

        draw_grid(current_step, playing)

        bpm_text = small.render(f"BPM: {bpm} (Up/Down)", True, TEXT)
        screen.blit(bpm_text, (WIDTH - 180, 15))

        status = "PLAYING" if playing else "STOPPED"
        status_color = ACTIVE if playing else DIM
        status_text = small.render(status, True, status_color)
        screen.blit(status_text, (WIDTH - 180, 35))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()