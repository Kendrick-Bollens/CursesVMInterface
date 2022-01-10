import curses


class Display:
    def __init__(self, stdscr: 'curses._CursesWindow'):
        self.stdscr = stdscr
        self.stdscr.nodelay(1)  # disable wait for user input

    def printVMSelectMenu(self, domains, cursorline):
        # self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, "Choose Your OS")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(domains)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printSelectedVMMenuStopped(self, vmname, options, cursorline):
        # self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, vmname + ": Stopped")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(options)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printSelectedVMMenuStarted(self, vmname, options, cursorline):
        # self.stdscr.erase()  # erase the old contents of the window
        self.stdscr.addstr(0, 0, vmname + ": Running")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.stdscr.addstr(2, 0, "↑/UP, ↓/DOWN, ENTER/CHOOSE")
        self.stdscr.clrtoeol()  # clear the rest of the line
        self.printOptions(options)
        self.updateCursor(cursorline)
        self.stdscr.refresh()

    def printError(self, error, currentSelection):
        self.stdscr.addstr(1, 0, error)
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