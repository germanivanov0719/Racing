#! python3

# How to use:
# ./check-lines.py main.py resources/Vehicles/* gameplay/start_menu/* gameplay/car_menu/*

import sys

args = list(sys.argv)[1:]

r = 0
if len(args) == 0:
    print("Filenames not detected.")
    exit(0)

i = 0
while i < len(args):
    try:
        open(args[i], 'r', encoding='utf-8')
    except Exception:
        print(f"File '{args[i]}' not found.")
        print('Trying to continue anyways...')
        del args[i]

    with open(args[i], 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        for s in lines:
            if s.strip() != "" and s.strip()[0] != '#':
                r += 1
    i += 1

print(r)
