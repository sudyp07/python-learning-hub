import random

FIRST_NAMES_MALE = [
    "James", "Liam", "Noah", "Ethan", "Lucas", "Mason", "Logan", "Owen",
    "Ryan", "Nathan", "Adam", "Caleb", "Daniel", "Marcus", "Victor", "Felix",
    "Diego", "Ravi", "Hiro", "Kenji", "Omar", "Yusuf", "Ivan", "Dmitri",
    "Aarav", "Vihaan", "Arjun", "Kai", "Leo", "Milo", "Ezra", "Silas"
]

FIRST_NAMES_FEMALE = [
    "Emma", "Olivia", "Ava", "Sophia", "Mia", "Isabella", "Chloe", "Lily",
    "Zoe", "Nora", "Aria", "Elena", "Maya", "Priya", "Ananya", "Sakura",
    "Yuki", "Aisha", "Fatima", "Layla", "Zara", "Ingrid", "Freya", "Astrid",
    "Rosa", "Camila", "Valentina", "Isla", "Ivy", "Ruby", "Hazel", "Iris"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "King", "Wright",
    "Patel", "Sharma", "Kumar", "Singh", "Tanaka", "Sato", "Kim", "Park",
    "Nguyen", "Tran", "Chen", "Wang", "Li", "Zhang", "Ivanov", "Petrov"
]

MIDDLE_INITIALS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

PREFIXES = ["Mr.", "Mrs.", "Ms.", "Dr.", "Prof."]
SUFFIXES = ["Jr.", "Sr.", "II", "III", "IV", "PhD", "MD", "Esq."]


def generate_name(gender=None, with_middle=False, with_prefix=False, with_suffix=False):
    if gender is None:
        gender = random.choice(["male", "female"])

    if gender == "male":
        first = random.choice(FIRST_NAMES_MALE)
    else:
        first = random.choice(FIRST_NAMES_FEMALE)

    last = random.choice(LAST_NAMES)

    parts = []

    if with_prefix:
        if gender == "male":
            parts.append(random.choice(["Mr.", "Dr.", "Prof."]))
        else:
            parts.append(random.choice(["Mrs.", "Ms.", "Dr.", "Prof."]))

    parts.append(first)

    if with_middle:
        parts.append(random.choice(MIDDLE_INITIALS) + ".")

    parts.append(last)

    if with_suffix:
        parts.append(random.choice(SUFFIXES))

    return ' '.join(parts)


def generate_username(first, last):
    styles = [
        f"{first.lower()}.{last.lower()}",
        f"{first.lower()}_{last.lower()}",
        f"{first.lower()}{last.lower()}",
        f"{first[0].lower()}{last.lower()}",
        f"{first.lower()}{last[0].lower()}",
        f"{first.lower()}{random.randint(1, 999)}",
        f"{last.lower()}.{first.lower()}",
    ]
    return random.choice(styles)


def generate_email(first, last, domain=None):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "icloud.com"]
    if domain is None:
        domain = random.choice(domains)

    styles = [
        f"{first.lower()}.{last.lower()}",
        f"{first.lower()}{last.lower()}",
        f"{first[0].lower()}{last.lower()}",
        f"{first.lower()}{random.randint(1, 99)}",
        f"{first.lower()}_{last.lower()}",
    ]
    return f"{random.choice(styles)}@{domain}"


def generate_full_profile():
    gender = random.choice(["male", "female"])
    name = generate_name(gender=gender, with_middle=True)
    first = name.split()[0]
    last = name.split()[-1]

    return {
        "name": name,
        "gender": gender,
        "username": generate_username(first, last),
        "email": generate_email(first, last),
        "age": random.randint(18, 75)
    }


def main():
    print("=== Random Name Generator ===\n")

    while True:
        print("1. Generate simple name")
        print("2. Generate name with middle initial")
        print("3. Generate name with prefix and suffix")
        print("4. Generate full profile (name + email + username)")
        print("5. Generate 10 random names")
        print("6. Quit")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            gender = input("Gender (m/f/any): ").strip().lower()
            g = None if gender == 'any' or not gender else ("male" if gender == 'm' else "female")
            print(f"\n  {generate_name(gender=g)}\n")

        elif choice == '2':
            gender = input("Gender (m/f/any): ").strip().lower()
            g = None if gender == 'any' or not gender else ("male" if gender == 'm' else "female")
            print(f"\n  {generate_name(gender=g, with_middle=True)}\n")

        elif choice == '3':
            gender = input("Gender (m/f/any): ").strip().lower()
            g = None if gender == 'any' or not gender else ("male" if gender == 'm' else "female")
            name = generate_name(gender=g, with_middle=True, with_prefix=True, with_suffix=True)
            print(f"\n  {name}\n")

        elif choice == '4':
            profile = generate_full_profile()
            print("\n  --- Profile ---")
            for key, val in profile.items():
                print(f"  {key.capitalize():10}: {val}")
            print()

        elif choice == '5':
            print()
            for i in range(10):
                print(f"  {i+1}. {generate_name(with_middle=random.choice([True, False]))}")
            print()

        elif choice == '6':
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()