import curses
from curses import wrapper

def getTime(stdscr):
    newAlarm = ""
    key = getKey(stdscr)
    if len(newAlarm) >= 4:
        return newAlarm
    elif(isinstance(key, int)):
        newAlarm = newAlarm + key
    elif key == 'ENTER':
        return newAlarm


def getKey(stdscr):
    # Store the key value in the variable `c`
    c = stdscr.getch()
    # Clear the terminal
    # stdscr.clear()
    if c == 113:
        return 1
    elif c == 114:
        return 2
    elif c == 115:
        return 3
    elif c == 116:
        return 4
    elif c == 117:
        return 5
    elif c == 118:
        return 6
    elif c == 119:
        return 7
    elif c == 120:
        return 8
    elif c == 121:
        return 9
    elif c == 112:
        return 0
    elif c == curses.KEY_ENTER:
        return 'ENTER'

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # Proceed with your program
    print("Running some program")
    while True:
        print(getTime(stdscr))




        # # Store the key value in the variable `c`
        # c = stdscr.getch()
        # # print(c);
        # # print(curses.keyname(c))
        # # Clear the terminal
        # stdscr.clear()
        # if c == 113:
        #     stdscr.addstr("You pressed the '1' key.")
        # elif c == 114:
        #     stdscr.addstr("You pressed the '2' key.")
        # elif c == 115:
        #     stdscr.addstr("You pressed the '3' key.")
        # elif c == 116:
        #     stdscr.addstr("You pressed the '4' key.")
        # elif c == 117:
        #     stdscr.addstr("You pressed the '5' key.")
        # elif c == 118:
        #     stdscr.addstr("You pressed the '6' key.")
        # elif c == 119:
        #     stdscr.addstr("You pressed the '7' key.")
        # elif c == 120:
        #     stdscr.addstr("You pressed the '8' key.")
        # elif c == 121:
        #     stdscr.addstr("You pressed the '9' key.")
        # elif c == 112:
        #     stdscr.addstr("You pressed the '0' key.")
        # elif c == curses.KEY_ENTER:
        #     stdscr.addstr("You pressed the 'Enter' key.")

        # ignore unknown input
        # else:
            # stdscr.addstr("This program doesn't know that key.....")
            # print(c)


# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)