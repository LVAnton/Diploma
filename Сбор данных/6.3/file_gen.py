import os
def create_files():
    for i in range(1, 41):
        filename = f"{i} лист.txt"
        with open(filename, "w") as file:
            file.write("")
create_files()