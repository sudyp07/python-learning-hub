import imaplib
import smtplib
import email
import ssl
import time
import os
import re
from email.mime.text import MIMEText
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime

# --- Config ---

IMAP_SERVERS = {
    "gmail.com": "imap.gmail.com",
    "outlook.com": "outlook.office365.com",
    "hotmail.com": "outlook.office365.com",
    "yahoo.com": "imap.mail.yahoo.com",
    "icloud.com": "imap.mail.me.com",
    "zoho.com": "imap.zoho.com",
    "aol.com": "imap.aol.com",
}

SMTP_SERVERS = {
    "gmail.com": ("smtp.gmail.com", 587),
    "outlook.com": ("smtp-mail.outlook.com", 587),
    "hotmail.com": ("smtp-mail.outlook.com", 587),
    "yahoo.com": ("smtp.mail.yahoo.com", 587),
    "icloud.com": ("smtp.mail.me.com", 587),
    "zoho.com": ("smtp.zoho.com", 587),
    "aol.com": ("smtp.aol.com", 587),
}


def guess_imap(email_addr):
    domain = email_addr.split("@")[-1].lower()
    return IMAP_SERVERS.get(domain)


def guess_smtp(email_addr):
    domain = email_addr.split("@")[-1].lower()
    return SMTP_SERVERS.get(domain)


def decode_mime_header(header):
    if not header:
        return ""
    parts = decode_header(header)
    result = ""
    for content, enc in parts:
        if isinstance(content, bytes):
            try:
                result += content.decode(enc or "utf-8", errors="ignore")
            except (LookupError, UnicodeDecodeError):
                result += content.decode("utf-8", errors="ignore")
        else:
            result += content
    return result


def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if ctype == "text/plain" and "attachment" not in disp:
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                except Exception:
                    continue
    else:
        try:
            return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
        except Exception:
            return ""
    return ""


def load_rules(path="rules.txt"):
    rules = []
    if not os.path.isfile(path):
        return rules

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("---")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        rule = {}
        for line in block.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                rule[key.strip().lower()] = value.strip()
        if "keyword" in rule and "reply" in rule:
            rules.append(rule)

    return rules


def log_reply(log_path, sender, subject, rule_keyword):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Replied to {sender} | Subject: {subject} | Matched: {rule_keyword}\n")


def send_reply(smtp_host, smtp_port, user, password, to_addr, subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["In-Reply-To"] = ""
    msg["Auto-Submitted"] = "auto-replied"

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, [to_addr], msg.as_string())


def match_rule(subject, body, rules):
    text = (subject + " " + body).lower()
    for rule in rules:
        keyword = rule["keyword"].lower()
        if keyword in text:
            return rule
    return None


def main():
    print("=== Email Auto Responder ===\n")

    user = os.environ.get("EMAIL_USER") or input("Email: ").strip()
    password = os.environ.get("EMAIL_PASS") or input("Password/app password: ").strip()

    imap_host = guess_imap(user)
    if not imap_host:
        imap_host = input("IMAP host: ").strip()

    smtp_host, smtp_port = guess_smtp(user) or (None, None)
    if not smtp_host:
        smtp_host = input("SMTP host: ").strip()
        smtp_port = int(input("SMTP port: ").strip())

    print(f"\nIMAP: {imap_host}")
    print(f"SMTP: {smtp_host}:{smtp_port}")

    rules = load_rules()
    if not rules:
        print("\nNo rules found in rules.txt. Creating sample file...")
        with open("rules.txt", "w", encoding="utf-8") as f:
            f.write(
                "keyword: pricing\n"
                "reply: Thanks for reaching out about pricing! Our team will send a detailed quote within 24 hours.\n"
                "---\n"
                "keyword: support\n"
                "reply: We received your support request. A technician will contact you shortly.\n"
                "---\n"
                "keyword: unsubscribe\n"
                "reply: You have been removed from our mailing list. Sorry for the inconvenience.\n"
            )
        rules = load_rules()
        print(f"Created rules.txt with {len(rules)} sample rules.")

    print(f"Loaded {len(rules)} rules.\n")

    reply_subject_prefix = input("Reply subject prefix (default 'Re: '): ").strip() or "Re: "

    check_interval = 30
    try:
        check_interval = int(input("Check interval in seconds (default 30): ").strip() or "30")
    except ValueError:
        pass

    # track processed message IDs
    processed_file = "processed_ids.txt"
    processed_ids = set()
    if os.path.isfile(processed_file):
        with open(processed_file, "r", encoding="utf-8") as f:
            processed_ids = set(line.strip() for line in f)

    print(f"\nMonitoring inbox every {check_interval}s. Ctrl+C to stop.\n")

    try:
        while True:
            try:
                mail = imaplib.IMAP4_SSL(imap_host)
                mail.login(user, password)
                mail.select("INBOX")

                status, data = mail.search(None, "UNSEEN")
                if status != "OK":
                    print("Search failed.")
                    mail.logout()
                    time.sleep(check_interval)
                    continue

                ids = data[0].split()

                for num in ids:
                    status, msg_data = mail.fetch(num, "(RFC822)")
                    if status != "OK":
                        continue

                    raw = msg_data[0][1]
                    msg = email.message_from_bytes(raw)

                    msg_id = msg.get("Message-ID", "").strip()
                    if msg_id in processed_ids:
                        continue

                    from_header = decode_mime_header(msg.get("From", ""))
                    sender_name, sender_email = parseaddr(from_header)
                    subject = decode_mime_header(msg.get("Subject", ""))

                    if sender_email.lower() == user.lower():
                        processed_ids.add(msg_id)
                        continue

                    body = get_body(msg)
                    rule = match_rule(subject, body, rules)

                    if rule:
                        reply_subject = reply_subject_prefix + subject
                        reply_body = rule["reply"]
                        reply_body += f"\n\n---\nAuto-reply from {user}"
                        reply_body += f"\nOriginal subject: {subject}"

                        try:
                            send_reply(
                                smtp_host, smtp_port,
                                user, password,
                                sender_email,
                                reply_subject, reply_body
                            )
                            print(f"Replied to {sender_email} (rule: {rule['keyword']})")
                            log_reply("auto_reply_log.txt", sender_email, subject, rule["keyword"])
                        except Exception as e:
                            print(f"Failed to reply to {sender_email}: {e}")
                    else:
                        print(f"No match for: {subject} from {sender_email}")

                    processed_ids.add(msg_id)
                    with open(processed_file, "a", encoding="utf-8") as f:
                        f.write(msg_id + "\n")

                mail.logout()

            except imaplib.IMAP4.error as e:
                print(f"IMAP error: {e}")
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n\nStopped.")


if __name__ == "__main__":
    main()