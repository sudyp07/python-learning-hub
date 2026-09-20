import cv2
import numpy as np
import sys

try:
    import mediapipe as mp
except ImportError:
    print("Install: pip install mediapipe opencv-python")
    sys.exit(1)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_PIPS = [3, 6, 10, 14, 18]


def count_fingers(hand_landmarks, handedness):
    fingers_up = []

    # Thumb (compare x positions depending on hand)
    if handedness == "Right":
        fingers_up.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)
    else:
        fingers_up.append(1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0)

    # Other 4 fingers (tip above pip => up)
    for tip, pip in zip(FINGER_TIPS[1:], FINGER_PIPS[1:]):
        fingers_up.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

    return fingers_up


def recognize_gesture(fingers, landmarks):
    total = sum(fingers)

    # look for common gestures
    if total == 0:
        return "Fist"

    if total == 5:
        return "Open Palm"

    if fingers == [0, 1, 0, 0, 0]:
        return "Pointing Up"

    if fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up"

    if fingers == [0, 1, 1, 0, 0]:
        return "Peace"

    if fingers == [0, 1, 0, 0, 1]:
        return "Rock"

    if fingers == [1, 1, 0, 0, 1]:
        return "I Love You"

    if fingers == [1, 1, 0, 0, 0]:
        return "Gun"

    if fingers == [1, 1, 1, 0, 0]:
        return "Three"

    if fingers == [0, 1, 1, 1, 0]:
        return "Three Up"

    if fingers == [0, 1, 1, 1, 1]:
        return "Four"

    if fingers == [1, 1, 1, 1, 1]:
        return "Five"

    if fingers == [0, 0, 0, 0, 1]:
        return "Pinky"

    if fingers == [1, 0, 0, 0, 1]:
        return "Horns"

    if fingers == [1, 1, 0, 0, 0]:
        return "Two Up"

    return f"{total} fingers"


def get_landmark_list(hand_landmarks):
    return [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]


def fingers_to_string(fingers):
    names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    up = [names[i] for i, v in enumerate(fingers) if v]
    down = [names[i] for i, v in enumerate(fingers) if not v]
    return up, down


def main():
    print("=== Hand Gesture Recognizer ===\n")
    print("Controls:")
    print("  Q / ESC  - Quit")
    print("  S        - Save snapshot")
    print("  M        - Toggle mirror mode\n")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY)

    if not cap.isOpened():
        print("Could not open camera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    mirror = True
    snapshot_count = 0

    with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
        max_num_hands=2
    ) as hands:

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if mirror:
                frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = hands.process(rgb)
            rgb.flags.writeable = True

            h, w = frame.shape[:2]

            if results.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    handedness = "Right"
                    if results.multi_handedness and i < len(results.multi_handedness):
                        handedness = results.multi_handedness[i].classification[0].label
                        if mirror:
                            handedness = "Left" if handedness == "Right" else "Right"

                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    fingers = count_fingers(hand_landmarks, handedness)
                    gesture = recognize_gesture(fingers, hand_landmarks)
                    up, down = fingers_to_string(fingers)

                    # label box
                    box_x = 10
                    box_y = 60 + i * 180

                    cv2.rectangle(frame, (box_x, box_y), (box_x + 380, box_y + 170), (30, 30, 30), -1)
                    cv2.rectangle(frame, (box_x, box_y), (box_x + 380, box_y + 170), (0, 200, 220), 2)

                    cv2.putText(frame, f"Hand: {handedness}", (box_x + 12, box_y + 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
                    cv2.putText(frame, f"Gesture: {gesture}", (box_x + 12, box_y + 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 120), 2)
                    cv2.putText(frame, f"Fingers: {sum(fingers)}/5", (box_x + 12, box_y + 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 220, 100), 2)

                    if up:
                        cv2.putText(frame, f"Up: {', '.join(up)}", (box_x + 12, box_y + 120),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 220, 255), 1)
                    if down:
                        cv2.putText(frame, f"Down: {', '.join(down)}", (box_x + 12, box_y + 145),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

                    # tip markers
                    for tip_idx in FINGER_TIPS:
                        lm = hand_landmarks.landmark[tip_idx]
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        is_up = fingers[FINGER_TIPS.index(tip_idx)]
                        color = (0, 255, 100) if is_up else (0, 0, 255)
                        cv2.circle(frame, (cx, cy), 12, color, -1)
            else:
                cv2.putText(frame, "No hand detected", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 100, 255), 2)

            # status bar
            cv2.putText(frame, "Q: quit  |  S: snapshot  |  M: mirror", (10, h - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            cv2.imshow("Hand Gesture Recognizer", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord('q'), 27):
                break
            elif key == ord('m'):
                mirror = not mirror
            elif key == ord('s'):
                snapshot_count += 1
                fname = f"gesture_snapshot_{snapshot_count}.png"
                cv2.imwrite(fname, frame)
                print(f"Saved {fname}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()