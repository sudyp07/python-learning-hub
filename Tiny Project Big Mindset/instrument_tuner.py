import numpy as np
import sounddevice as sd
import sys
import time

SAMPLE_RATE = 44100
BLOCK_SIZE = 4096

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

INSTRUMENTS = {
    "guitar": {
        "strings": [
            ("E2", 82.41), ("A2", 110.00), ("D3", 146.83),
            ("G3", 196.00), ("B3", 246.94), ("E4", 329.63)
        ]
    },
    "bass": {
        "strings": [
            ("E1", 41.20), ("A1", 55.00), ("D2", 73.42), ("G2", 98.00)
        ]
    },
    "ukulele": {
        "strings": [
            ("G4", 392.00), ("C4", 261.63), ("E4", 329.63), ("A4", 440.00)
        ]
    },
    "violin": {
        "strings": [
            ("G3", 196.00), ("D4", 293.66), ("A4", 440.00), ("E5", 659.25)
        ]
    },
    "cello": {
        "strings": [
            ("C2", 65.41), ("G2", 98.00), ("D3", 146.83), ("A3", 220.00)
        ]
    }
}


def freq_to_note(freq):
    if freq <= 0:
        return None, 0
    midi = 69 + 12 * np.log2(freq / 440.0)
    midi_rounded = int(round(midi))
    note_name = NOTES[midi_rounded % 12]
    octave = (midi_rounded // 12) - 1
    cents = (midi - midi_rounded) * 100
    return f"{note_name}{octave}", cents


def detect_pitch(audio):
    audio = audio.flatten()
    audio = audio - np.mean(audio)

    if np.max(np.abs(audio)) < 0.01:
        return -1

    corr = np.correlate(audio, audio, mode='full')
    corr = corr[len(corr) // 2:]

    d = np.diff(corr)
    try:
        start = np.where(d > 0)[0][0]
    except IndexError:
        return -1

    peak = np.argmax(corr[start:]) + start

    if peak == 0:
        return -1

    return SAMPLE_RATE / peak


def cents_bar(cents):
    position = int((cents + 50) / 100 * 41)
    position = max(0, min(40, position))
    bar = ['-'] * 41
    bar[20] = '|'
    bar[position] = 'O'
    return ''.join(bar)


def main():
    print("=== Instrument Tuner ===\n")
    print("Available instruments:")
    for i, name in enumerate(INSTRUMENTS.keys(), 1):
        print(f"  {i}. {name.capitalize()}")

    choice = input("\nChoose instrument: ").strip().lower()

    if choice.isdigit():
        keys = list(INSTRUMENTS.keys())
        idx = int(choice) - 1
        if 0 <= idx < len(keys):
            instrument = keys[idx]
        else:
            print("Invalid.")
            return
    else:
        instrument = choice

    if instrument not in INSTRUMENTS:
        print("Unknown instrument.")
        return

    print(f"\nTuning: {instrument.capitalize()}")
    print("Reference strings:")
    for note, freq in INSTRUMENTS[instrument]["strings"]:
        print(f"  {note}: {freq:.2f} Hz")

    print("\nPlay a note... (Ctrl+C to stop)\n")

    try:
        while True:
            audio = sd.rec(BLOCK_SIZE, samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()

            freq = detect_pitch(audio)

            if freq > 0:
                note, cents = freq_to_note(freq)
                status = "IN TUNE" if abs(cents) < 5 else ("TUNE UP" if cents < 0 else "TUNE DOWN")

                print(f"\r{freq:7.2f} Hz | {note:4} | {cents:+6.1f} cents | {status:9} | {cents_bar(cents)}", end='')

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n\nStopped.")


if __name__ == "__main__":
    main()