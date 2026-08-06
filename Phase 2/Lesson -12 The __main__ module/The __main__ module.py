# The main module in Python is written using the special variable __name__.

def main():
    print("Hello, World!")  #Hello, Sudip!
    print("This is the main function.")    #This is the main function.

if __name__ == "__main__":
    main()

"""
How it works
def main(): → Defines the main function.
if __name__ == "__main__": → Checks if the file is being run directly.
main() → Calls the main function.
"""

## lets make it more clear with it

def greet(name):
    print(f"Hello, {name}!")

def main():
    greet("Sudip")  #Hello, Sudip!

if __name__ == "__main__":
    main()