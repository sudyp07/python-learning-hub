import smtplib
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr


PROVIDERS = {
    "gmail": ("smtp.gmail.com", 587),
    "outlook": ("smtp-mail.outlook.com", 587),
    "yahoo": ("smtp.mail.yahoo.com", 587),
    "protonmail": ("smtp.protonmail.com", 587),
    "icloud": ("smtp.mail.me.com", 587),
    "zoho": ("smtp.zoho.com", 587),
    "aol": ("smtp.aol.com", 587),
    "gmx": ("smtp.gmx.com", 587),
}


def guess_provider(email):
    domain = email.split("@")[-1].lower()
    for name, (host, port) in PROVIDERS.items():
        if name in domain:
            return host, port
    return None, None


def build_message(sender, recipient, subject, body, is_html=False, attachments=None, cc=None, bcc=None):
    msg = MIMEMultipart()
    msg["From"] = formataddr(("", sender))
    msg["To"] = recipient
    msg["Subject"] = subject

    if cc:
        msg["Cc"] = cc

    if is_html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    if attachments:
        for path in attachments:
            if not os.path.isfile(path):
                print(f"  Skipping missing attachment: {path}")
                continue
            with open(path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(path)}"
            )
            msg.attach(part)

    return msg


def send_email(sender, password, recipient, subject, body,
               smtp_host=None, smtp_port=None, is_html=False,
               attachments=None, cc=None, bcc=None):

    if not smtp_host:
        smtp_host, smtp_port = guess_provider(sender)
        if not smtp_host:
            smtp_host = input("SMTP host: ").strip()
            smtp_port = int(input("SMTP port: ").strip())

    msg = build_message(sender, recipient, subject, body, is_html, attachments, cc, bcc)

    recipients = [recipient]
    if cc:
        recipients += [x.strip() for x in cc.split(",")]
    if bcc:
        recipients += [x.strip() for x in bcc.split(",")]

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())

    return True


def main():
    print("=== Email Sender ===\n")

    sender = os.environ.get("EMAIL_USER") or input("Your email: ").strip()
    password = os.environ.get("EMAIL_PASS") or input("Password/app password: ").strip()

    host, port = guess_provider(sender)
    if host:
        print(f"Detected SMTP: {host}:{port}")
        custom = input("Use this? (y/n): ").strip().lower()
        if custom != 'y':
            host = input("SMTP host: ").strip()
            port = int(input("SMTP port: ").strip())

    while True:
        print("\n--- New Email ---")
        recipient = input("To: ").strip()
        cc = input("Cc (blank): ").strip() or None
        bcc = input("Bcc (blank): ").strip() or None
        subject = input("Subject: ").strip()
        print("Body (type END on its own line to finish):")

        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        body = "\n".join(lines)

        is_html = input("Send as HTML? (y/n): ").strip().lower() == 'y'

        att_input = input("Attachments (comma-separated paths, blank for none): ").strip()
        attachments = [p.strip() for p in att_input.split(",")] if att_input else None

        try:
            send_email(
                sender, password, recipient, subject, body,
                smtp_host=host, smtp_port=port,
                is_html=is_html, attachments=attachments,
                cc=cc, bcc=bcc
            )
            print("Sent successfully.")
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Use an app password, not your regular password.")
        except Exception as e:
            print(f"Failed: {e}")

        again = input("\nSend another? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("Done.")


if __name__ == "__main__":
    main()