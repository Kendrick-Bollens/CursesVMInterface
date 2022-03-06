import curses


class Display(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho() # Disable key echoing
        curses.raw()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(1)  # disable wait for user input
        self.currentOptions = []
        self.currentError = ""

    def printVMSelectMenu(self, cursorline):
        self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, "Choose Your OS")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(1, 0, self.currentError)
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(self.currentOptions)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printSelectedVMMenuStopped(self, vmname, cursorline):
        self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, vmname + ": Stopped")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(1, 0, self.currentError)
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(self.currentOptions)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printSelectedVMMenuStarted(self, vmname, cursorline):
        self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, vmname + ": Running")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(1, 0, self.currentError)
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(self.currentOptions)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printReallyUpdateMenu(self,cursorline):
        self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, "This Update may require some time and will RESET all images are you sure that you want to do it")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(1, 0, self.currentError)
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(self.currentOptions)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printError(self, error, currentSelection):
        self.currentError = error
        self.stdscr.addstr(1, 0, self.currentError)
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.updateCursor(currentSelection)
        self.stdscr.refresh()

    def clearError(self, currentSelection):
        self.printError("", currentSelection)

    # generates the options Menu
    def printOptions(self, options):
        # os liste ausgeben
        i = 1
        # os liste ausgeben
        i = 0
        for option in options:
            self.stdscr.addstr(3 + i, 0, ' ' + option)
            self.stdscr.clrtobot()  # clear the rest of the line
            i += 1

    def disableCursor(self):
        curses.curs_set(0)

    def enableCursor(self):
        curses.curs_set(2)

    def updateCursor(self, currentSelection):
        # Move cursor to the selected line
        self.stdscr.move(3 + currentSelection, 0)

    def getInput(self):
        return self.stdscr.getch()