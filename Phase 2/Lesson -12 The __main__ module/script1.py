"""
script1.py

This file demonstrates how __name__ == "__main__" works.

Rule:
- If this file is run directly:
      python script1.py
  __name__ becomes "__main__"

- If this file is imported into another file:
      import script1
  __name__ becomes "script1"

Therefore, the code inside:

    if __name__ == "__main__":

runs ONLY when this file is executed directly.
"""


def main():
    """Main function of this program."""
    print("🍕 My favorite food is Pizza!")


print(f"Current __name__ value: {__name__}")

if __name__ == "__main__":
    print("\n✅ script1.py is running directly.")
    print("Calling main()...\n")
    main()
else:
    print("\n📦 script1.py was imported.")
    print("main() was NOT called automatically.\n")