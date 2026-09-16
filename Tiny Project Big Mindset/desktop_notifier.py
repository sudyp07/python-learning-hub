import sys
import time
import threading
import platform

OS = platform.system()

if OS == "Windows":
    try:
        from win10toast import ToastNotifier
        HAS_WIN10TOAST = True
    except ImportError:
        HAS_WIN10TOAST = False
    try:
        from plyer import notification
        HAS_PLYER = True
    except ImportError:
        HAS_PLYER = False
elif OS == "Darwin":
    HAS_PLYER = False
    try:
        from plyer import notification
        HAS_PLYER = True
    except ImportError:
        pass
else:
    try:
        from plyer import notification
        HAS_PLYER = True
    except ImportError:
        HAS_PLYER = False


def notify_windows(title, message, duration=5):
    if HAS_WIN10TOAST:
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=duration, threaded=True)
        return True
    if HAS_PLYER:
        notification.notify(title=title, message=message, timeout=duration)
        return True
    return False


def notify_plyer(title, message, duration=5):
    if HAS_PLYER:
        notification.notify(title=title, message=message, timeout=duration)
        return True
    return False


def notify_linux(title, message):
    import subprocess
    try:
        subprocess.run(["notify-send", title, message], check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def notify_mac(title, message):
    import subprocess
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def send_notification(title, message, duration=5):
    if OS == "Windows":
        if notify_windows(title, message, duration):
            return True
    elif OS == "Darwin":
        if notify_mac(title, message):
            return True
    elif OS == "Linux":
        if notify_linux(title, message):
            return True

    if notify_plyer(title, message, duration):
        return True

    print(f"[NOTIFICATION] {title}: {message}")
    return False


def schedule_notification(title, message, delay_seconds):
    def worker():
        time.sleep(delay_seconds)
        send_notification(title, message)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t


def main():
    print("=== Desktop Notifier ===\n")
    print(f"Platform: {OS}\n")

    while True:
        print("1. Send notification now")
        print("2. Schedule notification")
        print("3. Pomodoro timer")
        print("4. Water reminder")
        print("5. Quit")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            title = input("Title: ").strip() or "Notification"
            message = input("Message: ").strip() or "Hello!"
            send_notification(title, message)
            print("Sent.\n")

        elif choice == '2':
            title = input("Title: ").strip() or "Reminder"
            message = input("Message: ").strip() or "Time is up!"
            try:
                delay = int(input("Delay in seconds: ").strip())
            except ValueError:
                print("Invalid delay.\n")
                continue
            schedule_notification(title, message, delay)
            print(f"Scheduled in {delay}s.\n")

        elif choice == '3':
            try:
                work = int(input("Work minutes (default 25): ").strip() or "25")
                brk = int(input("Break minutes (default 5): ").strip() or "5")
                cycles = int(input("Cycles (default 3): ").strip() or "3")
            except ValueError:
                print("Invalid input.\n")
                continue

            def pomodoro():
                for i in range(cycles):
                    send_notification("Pomodoro", f"Cycle {i+1}: Focus for {work} min")
                    time.sleep(work * 60)
                    send_notification("Pomodoro", f"Cycle {i+1}: Break for {brk} min")
                    time.sleep(brk * 60)
                send_notification("Pomodoro", "All cycles complete!")

            threading.Thread(target=pomodoro, daemon=True).start()
            print("Pomodoro started in background.\n")

        elif choice == '4':
            try:
                interval = int(input("Remind every X minutes: ").strip())
            except ValueError:
                print("Invalid.\n")
                continue

            def water():
                while True:
                    time.sleep(interval * 60)
                    send_notification("Hydration", "Time to drink water!")

            threading.Thread(target=water, daemon=True).start()
            print(f"Water reminder every {interval} min.\n")

        elif choice == '5':
            break
        else:
            print("Invalid.\n")


if __name__ == "__main__":
    main()