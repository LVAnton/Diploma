import os


def create_files():
    """Creates 43 files named from "1 sheet" to "43 sheet"."""

    for i in range(1, 44):
        filename = f"{i} лист.txt"  # Or another extension if needed.

        try:
            with open(filename, "w") as file:
                # You can write something to the file here (e.g., an empty string)
                # If you need empty files, just creating them is sufficient.
                file.write("")
            print(f"File '{filename}' successfully created.")

        except Exception as e:
            print(f"Error creating file '{filename}': {e}")


# Call the function to create the files
create_files()