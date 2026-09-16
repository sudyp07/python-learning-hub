import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import base64

# --- Twilio SMS ---

def send_twilio(account_sid, auth_token, from_number, to_number, message):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    data = urlencode({
        "From": from_number,
        "To": to_number,
        "Body": message
    }).encode()

    auth = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()

    req = Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())

    return result


# --- Vonage (Nexmo) SMS ---

def send_vonage(api_key, api_secret, from_name, to_number, message):
    url = "https://rest.nexmo.com/sms/json"

    data = urlencode({
        "api_key": api_key,
        "api_secret": api_secret,
        "from": from_name,
        "to": to_number,
        "text": message
    }).encode()

    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())

    return result


# --- Textbelt (simple, no signup required for 1 free/day) ---

def send_textbelt(phone, message, api_key="textbelt"):
    url = "https://textbelt.com/text"

    data = urlencode({
        "phone": phone,
        "message": message,
        "key": api_key
    }).encode()

    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())

    return result


# --- Telegram (via bot, free) ---

def send_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode()

    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())

    return result


# --- CLI ---

def save_config(config):
    with open("sms_config.json", "w") as f:
        json.dump(config, f, indent=2)


def load_config():
    if os.path.isfile("sms_config.json"):
        try:
            with open("sms_config.json", "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def setup_twilio():
    print("\n--- Twilio Setup ---")
    print("Get credentials at https://www.twilio.com/console")
    sid = input("Account SID: ").strip()
    token = input("Auth Token: ").strip()
    from_num = input("Twilio phone number (e.g. +15551234567): ").strip()
    return {"provider": "twilio", "sid": sid, "token": token, "from": from_num}


def setup_vonage():
    print("\n--- Vonage Setup ---")
    print("Get credentials at https://dashboard.nexmo.com")
    key = input("API Key: ").strip()
    secret = input("API Secret: ").strip()
    from_name = input("Sender name or number: ").strip()
    return {"provider": "vonage", "key": key, "secret": secret, "from": from_name}


def setup_textbelt():
    print("\n--- Textbelt Setup ---")
    print("Free tier: 1 SMS per day. Get a key at https://textbelt.com/purchase")
    key = input("API Key (blank for free trial): ").strip() or "textbelt"
    return {"provider": "textbelt", "key": key}


def setup_telegram():
    print("\n--- Telegram Setup ---")
    print("1. Talk to @BotFather on Telegram to create a bot")
    print("2. Get your chat_id from @userinfobot")
    token = input("Bot token: ").strip()
    chat_id = input("Chat ID: ").strip()
    return {"provider": "telegram", "token": token, "chat_id": chat_id}


def send_with_config(config, to_number, message):
    provider = config.get("provider")

    if provider == "twilio":
        return send_twilio(config["sid"], config["token"], config["from"], to_number, message)

    if provider == "vonage":
        return send_vonage(config["key"], config["secret"], config["from"], to_number, message)

    if provider == "textbelt":
        return send_textbelt(to_number, message, config["key"])

    if provider == "telegram":
        return send_telegram(config["token"], config["chat_id"], message)

    raise ValueError(f"Unknown provider: {provider}")


def main():
    print("=== SMS Sender ===\n")

    config = load_config()

    if config:
        print(f"Loaded config: {config.get('provider')}")
        use_saved = input("Use saved config? (y/n): ").strip().lower()
        if use_saved != 'y':
            config = {}

    if not config:
        print("\nChoose SMS provider:")
        print("1. Twilio (paid, reliable)")
        print("2. Vonage/Nexmo (paid)")
        print("3. Textbelt (free tier, 1/day)")
        print("4. Telegram bot (free, requires app)")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            config = setup_twilio()
        elif choice == '2':
            config = setup_vonage()
        elif choice == '3':
            config = setup_textbelt()
        elif choice == '4':
            config = setup_telegram()
        else:
            print("Invalid.")
            return

        save_choice = input("Save config to sms_config.json? (y/n): ").strip().lower()
        if save_choice == 'y':
            save_config(config)
            print("Saved.")

    print(f"\nUsing provider: {config['provider']}")

    while True:
        if config["provider"] == "telegram":
            to_number = config["chat_id"]
            print(f"\nSending to chat_id: {to_number}")
        else:
            to_number = input("\nRecipient phone (with country code): ").strip()

        message = input("Message: ").strip()

        if not message:
            print("Empty message.")
            continue

        print("\nSending...")
        try:
            result = send_with_config(config, to_number, message)
            print(f"Response: {json.dumps(result, indent=2)}")

            if config["provider"] == "twilio":
                if result.get("sid"):
                    print("Sent successfully.")
                else:
                    print(f"Error: {result.get('message', 'unknown')}")

            elif config["provider"] == "vonage":
                messages = result.get("messages", [])
                if messages and messages[0].get("status") == "0":
                    print("Sent successfully.")
                else:
                    print(f"Error: {messages[0].get('error-text') if messages else 'unknown'}")

            elif config["provider"] == "textbelt":
                if result.get("success"):
                    print("Sent successfully.")
                else:
                    print(f"Error: {result.get('error')}")

            elif config["provider"] == "telegram":
                if result.get("ok"):
                    print("Sent successfully.")
                else:
                    print(f"Error: {result.get('description')}")

        except Exception as e:
            print(f"Failed: {e}")

        again = input("\nSend another? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("Done.")


if __name__ == "__main__":
    main()