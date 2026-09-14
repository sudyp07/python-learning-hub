import re

CARD_TYPES = {
    "Visa": {
        "patterns": [r'^4\d{12}(\d{3})?(\d{3})?$'],
        "lengths": [13, 16, 19],
        "cvv_len": 3
    },
    "MasterCard": {
        "patterns": [r'^5[1-5]\d{14}$', r'^2(2[2-9]|[3-6]\d|7[01]|720)\d{12}$'],
        "lengths": [16],
        "cvv_len": 3
    },
    "American Express": {
        "patterns": [r'^3[47]\d{13}$'],
        "lengths": [15],
        "cvv_len": 4
    },
    "Discover": {
        "patterns": [r'^6(?:011|5\d{2}|4[4-9]\d)\d{12}$'],
        "lengths": [16, 19],
        "cvv_len": 3
    },
    "JCB": {
        "patterns": [r'^(?:2131|1800|35\d{3})\d{11}$'],
        "lengths": [16, 17, 18, 19],
        "cvv_len": 3
    },
    "Diners Club": {
        "patterns": [r'^3(?:0[0-5]|[68]\d)\d{11}$'],
        "lengths": [14, 16, 19],
        "cvv_len": 3
    },
    "UnionPay": {
        "patterns": [r'^62\d{14,17}$'],
        "lengths": [16, 17, 18, 19],
        "cvv_len": 3
    },
    "Maestro": {
        "patterns": [r'^(5018|5020|5038|5893|6304|6759|676[1-3])\d{10,17}$'],
        "lengths": [12, 13, 14, 15, 16, 17, 18, 19],
        "cvv_len": 3
    }
}


def luhn_check(number):
    digits = [int(d) for d in number]
    digits.reverse()

    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    return total % 10 == 0


def detect_card_type(number):
    for name, info in CARD_TYPES.items():
        for pattern in info["patterns"]:
            if re.match(pattern, number):
                return name
    return None


def validate_card(number):
    cleaned = re.sub(r'[\s\-]', '', number)

    if not cleaned.isdigit():
        return False, "Contains non-digit characters", None

    if len(cleaned) < 12 or len(cleaned) > 19:
        return False, f"Invalid length ({len(cleaned)} digits)", None

    card_type = detect_card_type(cleaned)

    if card_type:
        expected_lengths = CARD_TYPES[card_type]["lengths"]
        if len(cleaned) not in expected_lengths:
            return False, f"{card_type} must be {expected_lengths} digits", card_type

    if not luhn_check(cleaned):
        return False, "Failed Luhn checksum (likely a fake number)", card_type

    return True, "Valid card number", card_type


def format_card(number):
    cleaned = re.sub(r'[\s\-]', '', number)
    groups = [cleaned[i:i+4] for i in range(0, len(cleaned), 4)]
    return ' '.join(groups)


def mask_card(number):
    cleaned = re.sub(r'[\s\-]', '', number)
    if len(cleaned) < 4:
        return cleaned
    return '*' * (len(cleaned) - 4) + cleaned[-4:]


def generate_check_digit(partial):
    digits = [int(d) for d in partial]
    digits.reverse()

    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    return str((10 - (total % 10)) % 10)


def main():
    print("=== Credit Card Validator ===\n")

    while True:
        raw = input("Card number (or 'quit'): ").strip()
        if raw.lower() in ('quit', 'exit', 'q'):
            break
        if not raw:
            continue

        valid, message, card_type = validate_card(raw)

        print(f"  Status: {'VALID' if valid else 'INVALID'}")
        print(f"  {message}")

        if card_type:
            print(f"  Card type: {card_type}")

        cleaned = re.sub(r'[\s\-]', '', raw)
        if cleaned.isdigit():
            print(f"  Formatted: {format_card(cleaned)}")
            print(f"  Masked:    {mask_card(cleaned)}")

        print()


if __name__ == "__main__":
    main()