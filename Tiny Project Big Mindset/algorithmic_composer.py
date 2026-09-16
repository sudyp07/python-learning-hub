import numpy as np
import wave
import random
import os
import sys

SAMPLE_RATE = 44100

# --- Music theory ---

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "pentatonic": [0, 2, 4, 7, 9],
    "blues": [0, 3, 5, 6, 7, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11]
}

CHORD_PROGRESSIONS = {
    "pop": [0, 4, 5, 3],
    "jazz": [1, 4, 0, 5],
    "blues": [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4],
    "classical": [0, 3, 4, 0],
    "emotional": [5, 3, 0, 4],
    "epic": [0, 5, 3, 4]
}


def note_to_freq(note, octave):
    index = NOTES.index(note)
    midi = (octave + 1) * 12 + index
    return 440.0 * (2 ** ((midi - 69) / 12))


def scale_notes(root_note, scale_name, num_octaves=2, base_octave=4):
    root_index = NOTES.index(root_note)
    intervals = SCALES[scale_name]

    result = []
    for oct_offset in range(num_octaves):
        for interval in intervals:
            idx = (root_index + interval) % 12
            oct_shift = (root_index + interval) // 12
            result.append((NOTES[idx], base_octave + oct_offset + oct_shift))

    return result


def chord_notes(root_note, chord_type, octave=4):
    root_index = NOTES.index(root_note)

    if chord_type == "major":
        intervals = [0, 4, 7]
    elif chord_type == "minor":
        intervals = [0, 3, 7]
    elif chord_type == "dim":
        intervals = [0, 3, 6]
    elif chord_type == "aug":
        intervals = [0, 4, 8]
    elif chord_type == "maj7":
        intervals = [0, 4, 7, 11]
    elif chord_type == "min7":
        intervals = [0, 3, 7, 10]
    elif chord_type == "dom7":
        intervals = [0, 4, 7, 10]
    else:
        intervals = [0, 4, 7]

    result = []
    for interval in intervals:
        idx = (root_index + interval) % 12
        oct_shift = (root_index + interval) // 12
        result.append((NOTES[idx], octave + oct_shift))

    return result


# --- Synthesis ---

def adsr_envelope(length, attack=0.01, decay=0.1, sustain=0.7, release=0.3):
    a = int(attack * SAMPLE_RATE)
    d = int(decay * SAMPLE_RATE)
    s = int(sustain * (length - a - d - int(release * SAMPLE_RATE)))
    r = length - a - d - s

    envelope = np.concatenate([
        np.linspace(0, 1, a),
        np.linspace(1, 0.6, d),
        np.full(s, 0.6),
        np.linspace(0.6, 0, r)
    ])

    if len(envelope) < length:
        envelope = np.pad(envelope, (0, length - len(envelope)))
    return envelope[:length]


def synth_note(freq, duration, wave_type="sine", volume=0.3):
    length = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, length, False)

    if wave_type == "sine":
        wave = np.sin(2 * np.pi * freq * t)
    elif wave_type == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "saw":
        wave = 2 * (t * freq - np.floor(0.5 + t * freq))
    elif wave_type == "triangle":
        wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    elif wave_type == "piano":
        wave = np.sin(2 * np.pi * freq * t)
        wave += 0.5 * np.sin(2 * np.pi * freq * 2 * t)
        wave += 0.25 * np.sin(2 * np.pi * freq * 3 * t)
        wave += 0.1 * np.sin(2 * np.pi * freq * 4 * t)
        wave /= 1.85
    elif wave_type == "pad":
        wave = np.sin(2 * np.pi * freq * t)
        wave += 0.3 * np.sin(2 * np.pi * freq * 1.005 * t)
        wave += 0.2 * np.sin(2 * np.pi * freq * 0.995 * t)
        wave /= 1.5
    else:
        wave = np.sin(2 * np.pi * freq * t)

    envelope = adsr_envelope(length)
    return wave * envelope * volume


def mix_track(total_length, events):
    buffer = np.zeros(total_length)

    for start_sample, samples in events:
        end_sample = start_sample + len(samples)
        if end_sample > total_length:
            samples = samples[:total_length - start_sample]
            end_sample = total_length
        buffer[start_sample:end_sample] += samples

    return buffer


def soft_clip(signal):
    return np.tanh(signal)


# --- Composition algorithms ---

def generate_melody(scale_notes_list, num_notes, rhythm_choices, rest_prob=0.15, step_prob=0.6):
    melody = []
    prev_index = len(scale_notes_list) // 2

    for _ in range(num_notes):
        if random.random() < rest_prob:
            duration = random.choice(rhythm_choices)
            melody.append((None, duration))
            continue

        # prefer stepwise motion
        if random.random() < step_prob:
            step = random.choice([-2, -1, 1, 2])
            new_index = max(0, min(len(scale_notes_list) - 1, prev_index + step))
        else:
            new_index = random.randint(0, len(scale_notes_list) - 1)

        note = scale_notes_list[new_index]
        duration = random.choice(rhythm_choices)
        melody.append((note, duration))
        prev_index = new_index

    return melody


def generate_bassline(progression, root_note, scale_name, beats_per_chord=4):
    bass = []
    root_index = NOTES.index(root_note)
    intervals = SCALES[scale_name]

    for chord_degree in progression:
        chord_root_idx = (root_index + intervals[chord_degree % len(intervals)]) % 12
        chord_root = NOTES[chord_root_idx]

        pattern = random.choice([
            [chord_root] * beats_per_chord,
            [chord_root, chord_root, chord_root + "", chord_root],
            [chord_root] + [None] * (beats_per_chord - 1)
        ])

        for n in pattern[:beats_per_chord]:
            bass.append((n, 1.0))

    return bass


def generate_chords(progression, root_note, scale_name, beats_per_chord=4):
    chords = []
    root_index = NOTES.index(root_note)
    intervals = SCALES[scale_name]

    for chord_degree in progression:
        degree_in_scale = chord_degree % len(intervals)
        interval = intervals[degree_in_scale]
        chord_root_idx = (root_index + interval) % 12
        chord_root = NOTES[chord_root_idx]

        # determine chord quality from scale
        if len(intervals) >= 7:
            third_idx = (degree_in_scale + 2) % len(intervals)
            fifth_idx = (degree_in_scale + 4) % len(intervals)

            third_interval = intervals[third_idx] - intervals[degree_in_scale]
            if third_interval < 0:
                third_interval += 12

            if third_interval == 3:
                chord_type = "minor"
            else:
                chord_type = "major"
        else:
            chord_type = random.choice(["major", "minor"])

        chord = chord_notes(chord_root, chord_type, octave=4)
        chords.append((chord, beats_per_chord))

    return chords


# --- WAV writer ---

def write_wav(filename, signal, sample_rate=SAMPLE_RATE):
    signal = np.clip(signal, -1, 1)
    data = (signal * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())


# --- Main composer ---

def compose(root_note, scale_name, progression_name, bpm, duration_sec, wave_type="piano", include_drums=True):
    beats_per_second = bpm / 60.0
    total_samples = int(SAMPLE_RATE * duration_sec)

    progression = CHORD_PROGRESSIONS[progression_name]
    scale_list = scale_notes(root_note, scale_name, num_octaves=2, base_octave=4)

    melody_rhythms = [0.25, 0.5, 0.5, 1.0, 1.0, 0.25, 0.75]
    if scale_name == "pentatonic" or scale_name == "blues":
        melody_rhythms = [0.25, 0.5, 0.25, 0.5, 0.75]

    total_beats = duration_sec * beats_per_second
    num_melody_notes = int(total_beats / 0.5)

    melody = generate_melody(scale_list, num_melody_notes, melody_rhythms)
    bassline = generate_bassline(progression, root_note, scale_name)
    chords = generate_chords(progression, root_note, scale_name)

    melody_events = []
    bass_events = []
    chord_events = []

    # melody timeline
    current_time = 0.0
    melody_notes_per_beat = 2

    for note, dur_beats in melody:
        if note is not None:
            freq = note_to_freq(note[0], note[1])
            samples = synth_note(freq, dur_beats / beats_per_second, wave_type, volume=0.25)
            melody_events.append((int(current_time * SAMPLE_RATE), samples))
        current_time += dur_beats / beats_per_second

    # bass timeline
    current_time = 0.0
    for note, dur_beats in bassline:
        if note is not None and current_time < duration_sec:
            freq = note_to_freq(note, 2)
            samples = synth_note(freq, dur_beats / beats_per_second, "saw", volume=0.2)
            bass_events.append((int(current_time * SAMPLE_RATE), samples))
        current_time += dur_beats / beats_per_second

    # chord timeline
    current_time = 0.0
    for chord, dur_beats in chords:
        for note in chord:
            if current_time < duration_sec:
                freq = note_to_freq(note[0], note[1])
                samples = synth_note(freq, dur_beats / beats_per_second, "pad", volume=0.08)
                chord_events.append((int(current_time * SAMPLE_RATE), samples))
        current_time += dur_beats / beats_per_second

    melody_track = mix_track(total_samples, melody_events)
    bass_track = mix_track(total_samples, bass_events)
    chord_track = mix_track(total_samples, chord_events)

    mixed = melody_track * 0.8 + bass_track * 0.7 + chord_track * 0.6

    if include_drums:
        kick_events = []
        snare_events = []
        hat_events = []

        kick_period = int(SAMPLE_RATE * 60 / bpm)
        snare_period = int(SAMPLE_RATE * 60 / bpm)
        hat_period = int(SAMPLE_RATE * 60 / bpm / 2)

        for i in range(0, total_samples, kick_period):
            if i + 10000 < total_samples:
                t = np.linspace(0, 0.15, int(SAMPLE_RATE * 0.15), False)
                freq = 150 * np.exp(-t * 25) + 40
                wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 10) * 0.5
                kick_events.append((i, wave))

        for i in range(snare_period, total_samples, snare_period):
            if i + 10000 < total_samples:
                t = np.linspace(0, 0.2, int(SAMPLE_RATE * 0.2), False)
                noise = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 12) * 0.25
                tone = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 20) * 0.15
                snare_events.append((i, noise + tone))

        for i in range(0, total_samples, hat_period):
            if i + 2000 < total_samples:
                t = np.linspace(0, 0.04, int(SAMPLE_RATE * 0.04), False)
                noise = np.random.uniform(-1, 1, len(t))
                noise = np.diff(noise, prepend=0) * np.exp(-t * 80) * 0.12
                hat_events.append((i, noise))

        kick_track = mix_track(total_samples, kick_events)
        snare_track = mix_track(total_samples, snare_events)
        hat_track = mix_track(total_samples, hat_events)

        mixed = mixed + kick_track + snare_track + hat_track

    mixed = soft_clip(mixed * 1.2) * 0.85
    return mixed


def main():
    print("=== Algorithmic Music Composer ===\n")

    root = input("Root note (C, D, E, F, G, A, B, or with #): ").strip().upper() or "C"
    if root not in NOTES:
        print(f"Invalid root note. Using C.")
        root = "C"

    print("\nAvailable scales:")
    for name in SCALES.keys():
        print(f"  - {name}")
    scale = input("Scale: ").strip().lower() or "minor"
    if scale not in SCALES:
        print("Unknown scale, using minor.")
        scale = "minor"

    print("\nAvailable progressions:")
    for name in CHORD_PROGRESSIONS.keys():
        print(f"  - {name}")
    prog = input("Progression: ").strip().lower() or "pop"
    if prog not in CHORD_PROGRESSIONS:
        print("Unknown progression, using pop.")
        prog = "pop"

    print("\nWave types: sine, square, saw, triangle, piano, pad")
    wave = input("Wave type for melody: ").strip().lower() or "piano"
    if wave not in ["sine", "square", "saw", "triangle", "piano", "pad"]:
        wave = "piano"

    try:
        bpm = int(input("BPM (default 100): ").strip() or "100")
    except ValueError:
        bpm = 100

    try:
        duration = float(input("Duration in seconds (default 20): ").strip() or "20")
    except ValueError:
        duration = 20.0

    include_drums = input("Add drums? (y/n, default y): ").strip().lower() != 'n'

    seed_input = input("Random seed (blank for random): ").strip()
    if seed_input:
        try:
            random.seed(int(seed_input))
            np.random.seed(int(seed_input))
        except ValueError:
            pass

    print(f"\nComposing: {root} {scale}, {prog} progression, {bpm} BPM, {duration}s...")

    signal = compose(root, scale, prog, bpm, duration, wave, include_drums)

    os.makedirs("compositions", exist_ok=True)
    filename = f"compositions/{root}_{scale}_{prog}_{random.randint(1000, 9999)}.wav"

    write_wav(filename, signal)
    print(f"\nSaved: {filename}")
    print(f"Size: {os.path.getsize(filename) / 1024:.1f} KB")


if __name__ == "__main__":
    main()