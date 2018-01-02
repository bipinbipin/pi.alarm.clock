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
        stdscr.clear()
        if c == 113:
            stdscr.addstr("You pressed the '1' key.")
        elif c == 114:
            stdscr.addstr("You pressed the '2' key.")
        elif c == 115:
            stdscr.addstr("You pressed the '3' key.")
        elif c == 116:
            stdscr.addstr("You pressed the '4' key.")
        elif c == 117:
            stdscr.addstr("You pressed the '5' key.")
        elif c == 118:
            stdscr.addstr("You pressed the '6' key.")
        elif c == 119:
            stdscr.addstr("You pressed the '7' key.")
        elif c == 120:
            stdscr.addstr("You pressed the '8' key.")
        elif c == 121:
            stdscr.addstr("You pressed the '9' key.")
        elif c == 112:
            stdscr.addstr("You pressed the '0' key.")
        elif c == curses.KEY_ENTER:
            stdscr.addstr("You pressed the 'Enter' key.")

        # ignore unknown input
        # else:
            # stdscr.addstr("This program doesn't know that key.....")
            # print(c)


# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)