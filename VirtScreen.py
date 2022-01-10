import curses
import time
from Display import Display
from VMManager import VMManager


def main() -> int:
    # Wrapped Main to not destroy anything cli related
    return curses.wrapper(c_main)


def c_main(stdscr: 'curses._CursesWindow') -> int:
    vscreen = VirtScreen(stdscr)
    while True:
        vscreen.updateScreen()
        vscreen.checkForUserInput()


class VirtScreen:
    vmStartedOptions = ["Stop", "Restart", "Force Stop (only when crashed)"]
    vmStoppedOptions = ["Start", "Reset", "Update", "Back to OS chooser"]

    def __init__(self, stdscr: 'curses._CursesWindow'):

        # Get the classes to Display and Manage the Vms
        self.vmManager = VMManager()
        self.display = Display(stdscr)

        # Set the defaults
        self.currentScreen = "MenuSelectVM"
        self.currentSelection = 0
        self.userCanSelect = 1  # describes if the user can select a option

    # update the screen corresponding if the user can choose a vm is selected or is running
    def updateScreen(self):

        if self.vmManager.getFirstActiveDomain() != None:
            self.currentScreen = "MenuVM"
            self.currentVM = self.vmManager.getFirstActiveDomain()

        # The Screen displays the Selection Menu
        if self.currentScreen == "MenuSelectVM":
            self.currentOptions = self.vmManager.getDomains()
            self.display.printVMSelectMenu(self.currentOptions, self.currentSelection)

        # If a VM is selected check open the Menu to it
        elif self.currentScreen == "MenuVM" and self.currentVM != None:

            # Check if the VM is running and if it is print the started menu
            if self.vmManager.getDomainActive(self.currentVM):
                self.currentOptions = VirtScreen.vmStartedOptions
                self.display.printSelectedVMMenuStarted(self.currentVM, self.currentOptions, self.currentSelection)

            # If it is not running print the stopped menu
            else:
                self.currentOptions = VirtScreen.vmStoppedOptions
                self.display.printSelectedVMMenuStopped(self.currentVM, self.currentOptions, self.currentSelection)

        # If a non existent menu is called reset to VMSelectMenu screen
        else:
            self.currentScreen = "MenuSelectVM"

    def checkForUserInput(self):
        # Catch input
        input = self.display.getInput()

        # check what the input means
        if input == curses.KEY_UP and self.userCanSelect == 1:
            if self.currentSelection > 0:
                self.currentSelection -= 1

        if input == curses.KEY_DOWN and self.userCanSelect == 1:
            if self.currentSelection < len(self.currentOptions) - 1:
                self.currentSelection += 1

        if input == 10 and self.userCanSelect == 1:
            self.optionSelection(self.currentOptions[self.currentSelection])

    def optionSelection(self, option):
        if option == "Start":
            self.display.printError("The VM is Starting", self.currentSelection)
            self.vmManager.startDomain(self.currentVM)
            self.waitUntilDomActiveChangend(1)

        elif option == "Stop":
            self.display.printError("The VM is Stopping", self.currentSelection)
            self.vmManager.stopDomain(self.currentVM)
            self.waitUntilDomActiveChangend(0)

        elif option == "Force Stop (only when crashed)":
            self.display.printError("The VM is Stopping", self.currentSelection)
            self.vmManager.forceStopDomain(self.currentVM)
            self.waitUntilDomActiveChangend(0)

        elif option == "Restart":
            self.display.printError("The VM is Restarting", self.currentSelection)
            self.vmManager.restartDomain(self.currentVM)
            time.sleep(20)
            self.waitUntilDomActiveChangend(1)

        elif option == "Update":
            self.display.printError("Not Implemented", self.currentSelection)

        elif option == "Reset":
            self.display.printError("Not Implemented", self.currentSelection)

        elif option == "Back to OS chooser":
            self.currentScreen = "MenuSelectVM"
            self.currentVM = None
        else:
            self.currentVM = option
            self.currentScreen = "MenuVM"

    def waitUntilDomActiveChangend(self, status, timeout=30, period=0.25):

        # Define Time to end
        mustend = time.time() + timeout

        # Disable the user input
        self.userCanSelect = 0
        self.display.disableCursor()

        # run as long the vm is starting/stopping or if the max time is overwritten
        while time.time() < mustend:

            # if the status changes break the loop and enable the cursor again
            if status == self.vmManager.getDomainActive(self.currentVM):
                self.display.clearError(self.currentSelection)
                self.display.enableCursor()
                self.userCanSelect = 1
                return True

            # sleep for slower polling rate
            time.sleep(period)

        # print error that it couldnt start/stop
        if status == 1:
            self.display.printError("The VM couldn't Start", self.currentSelection)
        if status == 0:
            self.display.printError("The VM couldn't Stop", self.currentSelection)

        # enable the user input and clear the error
        self.display.enableCursor()
        self.userCanSelect = 1

        # return that it didnt could change
        return False


if __name__ == '__main__':
    exit(main())
