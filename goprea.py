from executor import *
from interpreter import *

if __name__ == "__main__":
    print('start...')

    while True:
        command = input()
        if command == 'EXIT':
            break
        try:
            execute_query(parse_query(command))
        except Exception as e:
            print(e)