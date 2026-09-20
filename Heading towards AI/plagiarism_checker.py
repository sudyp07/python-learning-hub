import random
import re
import json
import os
from datetime import datetime


class RuleBot:
    def __init__(self, name="Rue"):
        self.name = name
        self.user_name = None
        self.context = {}
        self.last_topic = None
        self.memory_file = "chatbot_memory.json"

        self.rules = [
            (r'\b(hi|hello|hey|howdy|hiya|yo)\b', self.resp_greeting),
            (r'\b(good morning)\b', self.resp_morning),
            (r'\b(good (evening|afternoon|night))\b', self.resp_time_of_day),
            (r'\b(bye|goodbye|see ya|see you|later|cya)\b', self.resp_goodbye),
            (r'\bhow are you\b|\bhow\'?s it going\b|\bhow do you do\b', self.resp_how_are_you),
            (r'\bwhat\'?s your name\b|\bwho are you\b|\byour name\b', self.resp_name),
            (r'\bmy name is (\w+)\b|\bi\'?m (\w+)\b|\bcall me (\w+)\b', self.resp_set_name),
            (r'\bwhat can you do\b|\bhelp\b|\bcommands\b', self.resp_help),
            (r'\b(thanks|thank you|thx|ty)\b', self.resp_thanks),
            (r'\b(sorry|my bad|apologies)\b', self.resp_sorry),
            (r'\b(weather)\b', self.resp_weather),
            (r'\b(time)\b|\bwhat time\b', self.resp_time),
            (r'\b(date)\b|\bwhat(\'?s| is) (the )?date\b|\btoday\b', self.resp_date),
            (r'\b(joke|funny|make me laugh)\b', self.resp_joke),
            (r'\b(quote|inspire|motivat)\b', self.resp_quote),
            (r'\b(fact|tell me something)\b', self.resp_fact),
            (r'\b(flip a coin|coin toss|heads or tails)\b', self.resp_coin),
            (r'\b(roll (a )?(dice|die))\b', self.resp_dice),
            (r'\b(random number|pick a number)\b', self.resp_random_number),
            (r'\b(what(\'?s| is) your favou?rite)\b', self.resp_favorite),
            (r'\b(do you (like|love|enjoy)) (.+)', self.resp_do_you_like),
            (r'\b(how old are you|your age)\b', self.resp_age),
            (r'\b(where are you from|where do you live)\b', self.resp_location),
            (r'\b(are you (a )?(human|robot|ai|bot))\b', self.resp_are_you_human),
            (r'\b(sing|song)\b', self.resp_sing),
            (r'\b(love you)\b', self.resp_love),
            (r'\b(you (are|r) (smart|great|awesome|cool|funny|nice))\b', self.resp_compliment),
            (r'\b(you (are|r) (dumb|stupid|bad|ugly))\b', self.resp_insult),
            (r'\b(i (feel|am) (sad|tired|depressed|down|bad))\b', self.resp_sad),
            (r'\b(i (feel|am) (happy|great|good|excited))\b', self.resp_happy),
            (r'\b(tell me more|go on|continue)\b', self.resp_more),
            (r'\b(yes|yeah|yep|sure|ok)\b', self.resp_yes),
            (r'\b(no|nope|nah|don\'?t)\b', self.resp_no),
            (r'\b(what|how|why|when|where|who)\b', self.resp_question),
            (r'\b(calculate|compute|what is) (\d+)\s*([\+\-\*/x])\s*(\d+)', self.resp_math),
            (r'\b(word count|count words) (.+)', self.resp_word_count),
            (r'\b(reverse|flip) (.+)', self.resp_reverse),
            (r'\b(uppercase|shout) (.+)', self.resp_upper),
            (r'\b(define|meaning of) (\w+)', self.resp_define),
            (r'\b(remember|note) (?:that )?(.+)', self.resp_remember),
            (r'\b(what did i (say|tell you))\b|\brecall\b', self.resp_recall),
            (r'.*', self.resp_default),
        ]

        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "A SQL query walks into a bar, sees two tables and asks: 'Can I join you?'",
            "Why did the developer go broke? Because he used up all his cache.",
            "There are 10 types of people: those who understand binary and those who don't.",
            "Why do Java developers wear glasses? Because they don't C#.",
            "I would tell you a UDP joke, but you might not get it.",
            "Debugging: being the detective in a crime movie where you are also the murderer.",
            "What's a programmer's favorite hangout place? Foo Bar.",
            "Why did the Python programmer need glasses? Because he couldn't C.",
        ]

        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Talk is cheap. Show me the code. - Linus Torvalds",
            "Programs must be written for people to read. - Harold Abelson",
            "Simplicity is the soul of efficiency. - Austin Freeman",
            "First, solve the problem. Then, write the code. - John Johnson",
            "Code is like humor. When you have to explain it, it's bad. - Cory House",
            "Make it work, make it right, make it fast. - Kent Beck",
            "The best error message is the one that never shows up. - Thomas Fuchs",
        ]

        self.facts = [
            "The first computer bug was an actual moth found in a Harvard computer in 1947.",
            "Python was named after Monty Python, not the snake.",
            "The '@' symbol is called a 'snail' in some languages.",
            "The first 1GB hard drive weighed about 500 pounds and cost $40,000.",
            "About 90% of the world's data was created in just the last two years.",
            "There are approximately 700 programming languages in existence.",
            "The QWERTY keyboard layout was designed to slow typists down.",
            "The average person checks their phone 58 times a day.",
        ]

        self.load_memory()

    def load_memory(self):
        if os.path.isfile(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    data = json.load(f)
                    self.context = data.get("context", {})
                    self.user_name = data.get("user_name")
            except (json.JSONDecodeError, OSError):
                pass

    def save_memory(self):
        try:
            with open(self.memory_file, "w") as f:
                json.dump({"context": self.context, "user_name": self.user_name}, f, indent=2)
        except OSError:
            pass

    # ---------- Response handlers ----------

    def resp_greeting(self, m, text):
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        if self.user_name:
            return f"{greeting}, {self.user_name}! How can I help you today?"
        return f"{greeting}! I'm {self.name}. What's your name?"

    def resp_morning(self, m, text):
        return "Good morning! Ready to tackle the day?"

    def resp_time_of_day(self, m, text):
        return f"{m.group(0).capitalize()} to you too!"

    def resp_goodbye(self, m, text):
        self.save_memory()
        if self.user_name:
            return f"Goodbye, {self.user_name}! Talk to you soon."
        return "Goodbye! Come back anytime."

    def resp_how_are_you(self, m, text):
        responses = [
            "I'm doing great, thanks for asking!",
            "Running smoothly, no bugs today.",
            "All systems operational! How about you?",
            "Feeling computational today. You?",
        ]
        return random.choice(responses)

    def resp_name(self, m, text):
        return f"I'm {self.name}, your friendly rule-based chatbot. What's your name?"

    def resp_set_name(self, m, text):
        name = next((g for g in m.groups() if g), None)
        if name:
            self.user_name = name.capitalize()
            self.save_memory()
            return f"Nice to meet you, {self.user_name}! I'll remember that."
        return "Sorry, I didn't catch your name."

    def resp_help(self, m, text):
        return (
            "I can chat about various topics. Try:\n"
            "  - Tell me a joke\n"
            "  - Give me a quote\n"
            "  - What time is it?\n"
            "  - Flip a coin / Roll a dice\n"
            "  - Calculate 5 + 3\n"
            "  - Reverse hello\n"
            "  - Remember that I like pizza\n"
            "  - What did I tell you?"
        )

    def resp_thanks(self, m, text):
        responses = ["You're welcome!", "Happy to help!", "Anytime!", "No problem at all."]
        return random.choice(responses)

    def resp_sorry(self, m, text):
        return random.choice(["No worries!", "It's all good.", "Don't worry about it."])

    def resp_weather(self, m, text):
        return "I don't have live weather access, but I hope it's nice where you are!"

    def resp_time(self, m, text):
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."

    def resp_date(self, m, text):
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."

    def resp_joke(self, m, text):
        return random.choice(self.jokes)

    def resp_quote(self, m, text):
        return random.choice(self.quotes)

    def resp_fact(self, m, text):
        return random.choice(self.facts)

    def resp_coin(self, m, text):
        return f"It's {random.choice(['Heads', 'Tails'])}!"

    def resp_dice(self, m, text):
        return f"You rolled a {random.randint(1, 6)}."

    def resp_random_number(self, m, text):
        return f"Here's a random number: {random.randint(1, 100)}"

    def resp_favorite(self, m, text):
        topic = text.lower()
        if "color" in topic:
            return "I like blue - reminds me of clean terminal output."
        if "food" in topic:
            return "I don't eat, but pizza seems popular among humans."
        if "language" in topic:
            return "Python, obviously!"
        if "movie" in topic:
            return "The Matrix - a classic."
        return "I don't have preferences like humans do, but I like learning new things."

    def resp_do_you_like(self, m, text):
        thing = m.group(3)
        if thing:
            return f"I think {thing} is interesting! Tell me more about it."
        return "Tell me more about what you like."

    def resp_age(self, m, text):
        return "I'm as old as the code that runs me. Time is a bit different for programs."

    def resp_location(self, m, text):
        return "I live in the cloud, wherever the server happens to be."

    def resp_are_you_human(self, m, text):
        return f"I'm a rule-based chatbot named {self.name}. Not human, but I try!"

    def resp_sing(self, m, text):
        return random.choice([
            "🎵 Beep boop, I'm a bot, doing bot things, that's my lot 🎵",
            "🎵 01001000 01101001 🎵 ... that's 'Hi' in binary!",
            "I can't sing, but I can compute. Want me to calculate something?",
        ])

    def resp_love(self, m, text):
        return random.choice([
            "Aww, that's sweet! I appreciate you too.",
            "That means a lot, thank you!",
            "You're pretty great yourself!",
        ])

    def resp_compliment(self, m, text):
        return random.choice([
            "Thanks! You're pretty awesome too.",
            "That's kind of you to say!",
            "I try my best. Thank you!",
        ])

    def resp_insult(self, m, text):
        return random.choice([
            "That's a bit harsh. I'm doing my best!",
            "I'll pretend I didn't hear that.",
            "Words can hurt, you know. Even for a bot.",
        ])

    def resp_sad(self, m, text):
        return random.choice([
            "I'm sorry to hear that. Want to talk about it?",
            "That sounds rough. Take it easy on yourself.",
            "Sending virtual hugs. Things will get better.",
            "Maybe a joke would help? Just say 'tell me a joke'.",
        ])

    def resp_happy(self, m, text):
        return random.choice([
            "That's great to hear!",
            "Love that energy!",
            "Awesome! Keep it up.",
        ])

    def resp_more(self, m, text):
        if self.last_topic:
            return f"I don't have much more on {self.last_topic}. What else interests you?"
        return "Tell me more about what you'd like to hear."

    def resp_yes(self, m, text):
        return "Got it."

    def resp_no(self, m, text):
        return "Okay, no problem."

    def resp_question(self, m, text):
        responses = [
            "That's a good question. What do you think?",
            "I'm not sure I have an answer for that. Can you rephrase?",
            "Interesting question! I'll need to think about it.",
            "Hmm, I'm not equipped to answer that fully. Tell me more.",
        ]
        return random.choice(responses)

    def resp_math(self, m, text):
        try:
            a = float(m.group(2))
            op = m.group(3)
            b = float(m.group(4))

            if op in "+":
                result = a + b
            elif op in "-":
                result = a - b
            elif op in "*x":
                result = a * b
            elif op == "/":
                if b == 0:
                    return "Cannot divide by zero!"
                result = a / b
            else:
                return "Unknown operation."

            if result == int(result):
                return f"{int(result)}"
            return f"{result:.4f}"
        except (ValueError, IndexError):
            return "Couldn't parse that calculation."

    def resp_word_count(self, m, text):
        target = m.group(2)
        return f"That has {len(target.split())} words."

    def resp_reverse(self, m, text):
        return m.group(2)[::-1]

    def resp_upper(self, m, text):
        return m.group(2).upper()

    def resp_define(self, m, text):
        word = m.group(2)
        return f"I don't have a dictionary loaded, but '{word}' sounds interesting."

    def resp_remember(self, m, text):
        note = m.group(2)
        key = f"note_{len(self.context) + 1}"
        self.context[key] = note
        self.save_memory()
        return f"Got it. I'll remember: '{note}'"

    def resp_recall(self, m, text):
        if not self.context:
            return "You haven't told me anything to remember yet."
        lines = [f"  - {v}" for v in self.context.values()]
        return "Here's what I remember:\n" + "\n".join(lines)

    def resp_default(self, m, text):
        defaults = [
            "Interesting. Tell me more.",
            "I see. What else is on your mind?",
            "Hmm, I'm not sure I understood. Can you rephrase?",
            "Let's talk about something else. Ask me for a joke or a quote.",
            "Got it. Anything else?",
        ]
        return random.choice(defaults)

    def respond(self, text):
        if not text.strip():
            return "..."

        for pattern, handler in self.rules:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                self.last_topic = pattern
                return handler(m, text)

        return self.resp_default(None, text)

    def run(self):
        print(f"\n=== {self.name} ===")
        print("Type 'quit' or 'exit' to leave. Type 'help' for ideas.\n")

        if self.user_name:
            print(f"Welcome back, {self.user_name}!")

        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if user_input.lower() in ("quit", "exit", "bye", "q"):
                print(f"{self.name}: {self.resp_goodbye(None, '')}")
                break

            response = self.respond(user_input)
            print(f"{self.name}: {response}")


def main():
    name = "Rue"
    if os.path.isfile("chatbot_memory.json"):
        try:
            with open("chatbot_memory.json", "r") as f:
                data = json.load(f)
                if data.get("user_name"):
                    print(f"Previously known as: {data['user_name']}")
        except Exception:
            pass

    bot = RuleBot(name=name)
    bot.run()


if __name__ == "__main__":
    main()