import os


def print_directory_contents(path='.'):
    """
    Print the contents of a directory using the os module.

    Args:
        path (str): The directory path to list. Defaults to current directory.
    """
    try:
        # Get the list of all files and directories in the specified path
        contents = os.listdir(path)

        print(f"Contents of directory: {os.path.abspath(path)}")
        print("-" * 50)

        # Print each item in the directory
        for item in contents:
            item_path = os.path.join(path, item)

            # Check if it's a file or directory
            if os.path.isdir(item_path):
                print(f"[DIR]  {item}")
            else:
                # Get file size
                size = os.path.getsize(item_path)
                print(f"[FILE] {item} ({size} bytes)")

    except FileNotFoundError:
        print(f"Error: Directory '{path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    # Print current directory contents
    print_directory_contents()

    # You can also specify a different directory:
    # print_directory_contents('/path/to/your/directory')