import os
import time
import sys

TEXT_WIDTH = 110
LINE_BREAKS = 120


def set_width():
    if os.name == "posix":
        rows, columns = os.popen('stty size', 'r').read().split()
        TEXT_WIDTH = columns
        print("Text width is now: {}".format(TEXT_WIDTH))
    else:
        os.system("mode con cols=130")
        TEXT_WIDTH = 130
        print("Testing this {}".format(TEXT_WIDTH))


def split_input(user_string, chunk_size):
    output = []
    words = user_string.split(" ")
    total_length = 0

    while(total_length < len(user_string) and len(words) > 0):
        line = []
        next_word = words[0]
        line_len = len(next_word) + 1

        while(line_len < chunk_size) and len(words) > 0:
            words.pop(0)
            line.append(next_word)

            if (len(words) > 0):
                next_word = words[0]
                line_len += len(next_word) + 1

        line = " ".join(line)
        output.append(line)
        total_length += len(line)

    return output


def print_split(user_string, chunk_size=TEXT_WIDTH):
    output = split_input(user_string, chunk_size)
    for chunk in output:
        print(chunk)


def animate_text(split_text, speed):
    for segment in split_text:
        for letter in segment:
            sys.stdout.write(letter)
            time.sleep(speed)
        sys.stdout.write("\n")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


