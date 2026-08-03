spam_comments = [
    "Congratulations! You have won a free iPhone. Click here to claim your prize!",
    "Make $5000 per week working from home. No experience required!",
    "Amazing opportunity! Join now and earn unlimited money!",
    "You are selected as a lucky winner. Send your details to receive your reward.",
    "Click the link in my bio to get free followers instantly!",
    "Earn money fast with this simple trick. DM me now!",
    "Free crypto giveaway! Claim your coins before it's too late!",
    "Free money available! Click the link below!",
    "Invest $100 and get $1000 guaranteed return!",
    "Congratulations! Your account has been selected for a bonus.",
    "Check out this amazing product, you will love it!",
    "Get premium software for free. Download now!",
    "Your computer has a virus. Click here to fix it immediately!",
    "Exclusive deal just for you. Act fast!",
    "Become famous overnight with our promotion service!",
    "I made $10,000 in one week using this method!",
    "Send me your WhatsApp number for a special offer.",
    "Win free prizes every day. Register now!",
    "You are lucky today! Claim your free reward!",
    "Click this link to unlock your free membership!"
]


## taking user input from user !!
user_input = input("Enter a sweet comment: ")

## using if else statement to check the format
if user_input not in spam_comments:
    print(f"Sweet comment: {user_input}")
else:
    print(f"Spam comment Detected: {user_input}")