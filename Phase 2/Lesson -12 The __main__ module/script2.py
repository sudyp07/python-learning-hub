"""
script2.py

This file imports script1.

Notice:
script1.py is NOT the main program anymore.

Instead:
__name__ inside script1.py becomes "script1"

So:

if __name__ == "__main__":

becomes False.

That means main() is NOT called automatically.
"""

print("========== script2.py started ==========\n")

import script1

print("\n========== Back to script2.py ==========")

print("\nCalling script1.main() manually...\n")

script1.main()

print("\n========== script2.py finished ==========")