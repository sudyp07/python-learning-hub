# The main module in Python is written using the special variable __name__.

def main():
    print("Hello, World!")
    print("This is the main function.")

if __name__ == "__main__":
    main()

"""
How it works
def main(): → Defines the main function.
if __name__ == "__main__": → Checks if the file is being run directly.
main() → Calls the main function.
"""