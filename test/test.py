import curses
import time

stdscr=curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(10,10,'Hello')
stdscr.refresh()

time.sleep(1)

curses.nocbreak
stdscr.keypad(0)
curses.endwin()
