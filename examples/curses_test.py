import curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # Proceed with your program
    print("Running some program")
    while True:
        # Store the key value in the variable `c`
        c = stdscr.getch()
        print(c);
        print(c.isdigit())
        # Clear the terminal
        # stdscr.clear()
        if c == ord('a'):
            stdscr.addstr("You pressed the 'a' key.")
        elif c == curses.KEY_UP:
            stdscr.addstr("You pressed the up arrow.")
        else:
            stdscr.addstr("This program doesn't know that key.....")

def isNumber(c):
    c.isdigit()
# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)