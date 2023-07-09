import os

if __name__ == "__main__":

    for key, val in os.environ.items():
        print(key, '->', val)