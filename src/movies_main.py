import sys


def main():
    # how to process input queries.
    # this loop automatically terminates when EOF is reached from the file,
    # or the user enters ^D to terminate standard input
    for line in sys.stdin:
        line = line.strip()   # remove trailing newline
        print(line)


if __name__ == '__main__':
    main()