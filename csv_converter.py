import ast
from config import *


def square_to_move(square):
    """
    a1 - 0
    b1 - 1
    |
    h1 - 7
    a2 - 8
    |
    h8 - 63
    """
    left, right = square[0], square[1]
    # a -> 97
    left = ord(left) - 97
    right = 8*(int(right) - 1)
    return left + right


def write_file(name, text):
    with open(name, "w+") as file:
        file.write(text)
    return


def csvify(data, prefix=""):
    text = ""
    for k in data.keys():
        if isinstance(data[k], dict):
            text += csvify(data[k], str(prefix)+str(k)+",")
        else:
            text += prefix+str(k)+","+str(data[k])+"\n"
    return text


def run(key_names=None):
    message = "Turning data to csv "

    with open(DATA_NAME, "r") as file:
        text = file.read()
    data = ast.literal_eval(text)

    if key_names is None:
        key_names = data.keys()
    else:
        message += "using custom orders "

    print()
    print(message, end=f"({len(key_names)} files):\n")
    print(f"Saving to {CSV_STORAGE}")
    for k in key_names:
        header = CSV_HEADER_PREFIX + CSV_HEADERS[k]
        write_file(CSV_STORAGE+k+'.csv', header+"\n"+csvify(data[k]))
        print(f"-{k}")
    print()
    return
