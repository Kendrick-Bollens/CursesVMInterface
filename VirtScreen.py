import curses
import time
import os
import getpass
from Display import Display
from VMManager import VMManager


def start():
    while True:
        vscreen = VirtScreen()
        while True:
            vscreen.updateScreen()
            vscreen.checkForUserInput()
        curses.endwin()


class VirtScreen(object):
    vmStartedOptions = ["Stop", "Restart", "Force Stop (only when crashed)"]
    vmStoppedOptions = ["Start", "Start last state","Update", "Back to OS chooser"]
    reallyUpdateAllOptions = ["Dont update","I know the risk, update"]
    reallyUpdateVMOptions = ["Dont update","I know the risk, update"]
    reallyReloadVMOptions = ["Dont reload","I know the risk, reload"]
    MenuSelectVMOptions = ["Reload","Update", "Reboot"]


    def __init__(self):

        # Get the classes to Display and Manage the Vms
        self.vmManager = VMManager()
        self.display = Display()

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
            self.display.currentOptions = self.vmManager.getDomains()
            self.display.currentOptions.extend(VirtScreen.MenuSelectVMOptions)
            self.display.printVMSelectMenu(self.currentSelection)
            self.display.printError("The current user is: " + getpass.getuser())

        # If a VM is selected check open the Menu to it
        elif self.currentScreen == "MenuVM" and self.currentVM != None:

            # Check if the VM is running and if it is print the started menu
            if self.vmManager.getDomainActive(self.currentVM):
                self.display.currentOptions = VirtScreen.vmStartedOptions
                self.display.printSelectedVMMenuStarted(self.currentVM, self.currentSelection)

            # If it is not running print the stopped menu
            else:
                self.display.currentOptions = VirtScreen.vmStoppedOptions
                self.display.printSelectedVMMenuStopped(self.currentVM, self.currentSelection)

        # Reload All Screen
        elif self.currentScreen == "reallyReloadAll":
            self.display.currentOptions = VirtScreen.reallyReloadVMOptions
            self.display.printReallyReloadAllMenu(self.currentSelection)


        # Update ALl Screen
        elif self.currentScreen == "reallyUpdateAll":
            self.display.currentOptions = VirtScreen.reallyUpdateAllOptions
            self.display.printReallyUpdateAllMenu(self.currentSelection)
            
        # Update VM Screen
        elif self.currentScreen == "reallyUpdateVM":
            self.display.currentOptions = VirtScreen.reallyUpdateVMOptions
            self.display.printReallyUpdateVMMenu(self.currentSelection)

        # If a non existent menu is called reset to VMSelectMenu screen
        else:
            self.currentScreen = "MenuSelectVM"

    def checkForUserInput(self):
        # Catch input
        input = self.display.getInput()


        # check what the input means

        #Key Up
        if input == curses.KEY_UP and self.userCanSelect == 1:
            if self.currentSelection > 0:
                self.currentSelection -= 1

        #Key Down
        if input == curses.KEY_DOWN and self.userCanSelect == 1:
            if self.currentSelection < len(self.display.currentOptions) - 1:
                self.currentSelection += 1

        #Enter
        if input == 10 and self.userCanSelect == 1:
            self.optionSelection(self.display.currentOptions[self.currentSelection])
            self.currentSelection = 0

    def optionSelection(self, option):


        #Screen Options MenuVM Stopped

        if self.currentScreen == "MenuVM" and option == "Start":
            try:
                self.display.printError("The VM is Starting", self.currentSelection)
                self.vmManager.resetImg(self.currentVM)
                time.sleep(1)

                self.vmManager.startDomain(self.currentVM)
                self.waitUntilDomActiveChangend(1)
            except Exception as e:
                self.display.printError("Something went wrong with the Starting of the VM", self.currentSelection)

        elif self.currentScreen == "MenuVM" and option == "Start last state":
            try:
                self.display.printError("The VM is Starting", self.currentSelection)
                self.vmManager.startDomain(self.currentVM)
                self.waitUntilDomActiveChangend(1)
            except Exception as e:
                self.display.printError("Something went wrong with the Starting of the VM", self.currentSelection)

        elif self.currentScreen == "MenuVM" and option == "Back to OS chooser":
            self.currentScreen = "MenuSelectVM"
            self.currentVM = None
            

        #Screen Options MenuVM Started

        elif self.currentScreen == "MenuVM" and option == "Stop":
            try:
                self.display.printError("The VM is Stopping", self.currentSelection)
                self.vmManager.stopDomain(self.currentVM)
                self.waitUntilDomActiveChangend(0)
            except Exception as e:
                self.display.printError("Something went wrong with the Stopping of the VM", self.currentSelection)

        elif self.currentScreen == "MenuVM" and option == "Force Stop (only when crashed)":
            try:
                self.display.printError("The VM is Stopping", self.currentSelection)
                self.vmManager.forceStopDomain(self.currentVM)
                self.waitUntilDomActiveChangend(0)
            except Exception as e:
                self.display.printError("Something went wrong with the Stopping of the VM", self.currentSelection)


        elif self.currentScreen == "MenuVM" and option == "Restart":
            try:
                self.display.printError("The VM is Restarting", self.currentSelection)
                self.vmManager.restartDomain(self.currentVM)
                time.sleep(20)
                self.waitUntilDomActiveChangend(1)
            except Exception as e:
                self.display.printError("Something went wrong with the Restarting of the VM", self.currentSelection)


        # Screen Options ReallyUpdateAll
        elif self.currentScreen == "reallyReloadAllVM" and option == "I know the risk, reload":
            self.display.printError("VMs are Reloading", self.currentSelection)
            try:
                self.vmManager.redefineImage(self.currentVM)
                self.display.clearError(self.currentSelection)
            except Exception as e:
                self.display.printError("Something went wrong with the reload", self.currentSelection)
            self.currentScreen = "MenuVM"
            self.currentVM = None

        elif self.currentScreen == "reallyReloadVM" and option == "Dont reload":
            self.currentScreen = "MenuVM"
            self.currentVM = None



        # Screen Options ReallyUpdateVM

        elif self.currentScreen == "reallyUpdateVM" and option == "I know the risk, update":
            self.display.printError("VMs are Updating", self.currentSelection)
            try:
                self.vmManager.syncImg(self.currentVM)
                self.display.clearError(self.currentSelection)
                self.vmManager.redefineImage(self.currentVM)
            except Exception as e:
                self.display.printError("Something went wrong with the syncing", self.currentSelection)
            self.currentScreen = "MenuVM"

        elif self.currentScreen == "reallyUpdateVM" and option == "Dont update":
            self.currentScreen = "MenuVM"


        # Screen Options ReallyUpdateAll

        elif self.currentScreen == "reallyUpdateAll" and option == "I know the risk, update":
            self.display.printError("VMs are Updating", self.currentSelection)
            try:
                self.vmManager.syncAllImgs()
                self.display.clearError(self.currentSelection)
                self.vmManager.redefineAllImages()
            except Exception as e:
                self.display.printError("Something went wrong with the syncing", self.currentSelection)
            self.currentScreen = "MenuSelectVM"
            self.currentVM = None

        elif self.currentScreen == "reallyUpdateAll" and option == "Dont update":
            self.currentScreen = "MenuSelectVM"
            self.currentVM = None


        #Screen Options MenuSelectVM

        elif self.currentScreen == "MenuSelectVM" and option == "Reload":
            self.currentScreen = "reallyReloadVM"


        elif self.currentScreen == "MenuSelectVM" and option == "Update":
            self.currentScreen = "reallyUpdateAll"

        elif self.currentScreen == "MenuSelectVM" and option == "Reboot":
            os.system('reboot')

        elif self.currentScreen == "MenuSelectVM":
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


