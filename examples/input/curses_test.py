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
        # print(c);
        # print(curses.keyname(c))
        # Clear the terminal
        # stdscr.clear()
        if c == ord('1'):
            stdscr.addstr("You pressed the '1' key.")
        elif c == ord('2'):
            stdscr.addstr("You pressed the '2' key.")
        elif c == ord('3'):
            stdscr.addstr("You pressed the '3' key.")
        elif c == ord('4'):
            stdscr.addstr("You pressed the '4' key.")
        elif c == ord('5'):
            stdscr.addstr("You pressed the '5' key.")
        elif c == ord('6'):
            stdscr.addstr("You pressed the '6' key.")
        elif c == ord('7'):
            stdscr.addstr("You pressed the '7' key.")
        elif c == ord('8'):
            stdscr.addstr("You pressed the '8' key.")
        elif c == ord('9'):
            stdscr.addstr("You pressed the '9' key.")
        # elif c == curses.KEY_0:
        #     stdscr.addstr("You pressed the '0' key.")
        elif c == curses.KEY_ENTER:
            stdscr.addstr("You pressed the 'Enter' key.")
        else:
            stdscr.addstr("This program doesn't know that key.....")
            stdscr.addstr(c)

def isNumber(c):
    c.isdigit()
# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)