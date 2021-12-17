import curses
import sys
import libvirt
from xml.dom import minidom

# Text for Input Options
textInputoptions = "↑/UP, ↓/DOWN, ENTER/CHOOSE"

# Text for OS choosing
textOSAuswahl = "Choose Your OS"

# Text for Stopped VM Menu
testStoppedVMPreName = "VM "
testStoppedVMPostName = ": STOPPED"

# Text for Started VM Menu
testStartedVMPreName = "VM "
testStartedVMPostName = ": STARTED"


def main() -> int:
    # Wrapped Main to not destroy anything cli related
    return curses.wrapper(c_main)


def c_main(stdscr: 'curses._CursesWindow') -> int:
    generateOSauswahl(stdscr, getDomains())

    # end programm
    return 0


def generateHeadingText(stdscr, firstLine, secondLine, chosen="", error=""):
    stdscr.addstr(0, 0, firstLine + chosen)
    stdscr.addstr(1, 0, error)
    stdscr.addstr(2, 0, secondLine)


# generates the options Menu
def generateOptionsList(stdscr, options, selected, linestart=3) -> int:
    # os liste ausgeben
    i = 1
    # os liste ausgeben
    i = 0
    for option in options:
        stdscr.addstr(linestart + i, 0, ' ' + option)
        i += 1

    # Move cursor to the selected line
    stdscr.move(linestart + selected, 0)

    # return number of elements
    return i


def generateOSauswahl(stdscr, oses=["windows-objektorientierte-skriptsprachen", "windows-mediengestaltung",
                                    "windows-betriebsysteme-und-webcomputing",
                                    "linux-debian-grundlagen-des-cloud-computing"]):
    error = ""
    selected = 0
    while True:
        generateHeadingText(stdscr, textOSAuswahl, textInputoptions, error=error)
        generateOptionsList(stdscr, oses, selected)

        # Catch input
        input = stdscr.getch()

        if input == curses.KEY_UP:
            if selected > 0:
                selected -= 1

        if input == curses.KEY_DOWN:
            if selected < len(oses) - 1:
                selected += 1
        if input == 10:
            stdscr.clear()
            generateVmMenu(stdscr, oses[selected])
            selected = 0

        # clear screen to avoid overlap
        stdscr.clear()


def generateVmMenu(stdscr, vmname="Beispiel", optionsStopped=["Start", "Reset", "Update", "Back to OS chooser"],
                   optionsStatrtedd=["Stop", "Restart", "Force Stop (only when crashed"]):
    selected = 0
    error = ""
    vmStatus = 0  # 0 means stopped 1 means started
    while True:
        if vmStatus != getDomainActive(vmname):
            vmStatus = getDomainActive(vmname)
            error = ""

        if vmStatus == 0:
            # Generate Interface
            generateHeadingText(stdscr, testStoppedVMPreName + vmname + testStoppedVMPostName, textInputoptions,
                                error=error)
            generateOptionsList(stdscr, optionsStopped, selected)

            # Catch input
            input = stdscr.getch()

            # check what the input means
            if input == curses.KEY_UP:
                if selected > 0:
                    selected -= 1

            if input == curses.KEY_DOWN:
                if selected < len(optionsStopped) - 1:
                    selected += 1
            if input == 10:
                if selected == 0:
                    stdscr.clear()
                    selected = 0
                    startDomain(vmname)
                    error = "trying to start"
                if selected == 1:
                    stdscr.clear()
                    selected = 0
                    error = "Not Implemented yet"
                if selected == 2:
                    stdscr.clear()
                    selected = 0
                    error = "Not Implemented yet"
                if selected == 3:
                    stdscr.clear()
                    selected = 0
                    break

        if vmStatus == 1:
            # Generate Interface
            generateHeadingText(stdscr, testStartedVMPreName + vmname + testStartedVMPostName, textInputoptions,
                                error=error)
            generateOptionsList(stdscr, optionsStatrtedd, selected)

            # Catch input
            input = stdscr.getch()

            # check what the input means
            if input == curses.KEY_UP:
                if selected > 0:
                    selected -= 1

            if input == curses.KEY_DOWN:
                if selected < len(optionsStopped) - 1:
                    selected += 1
            if input == 10:
                if selected == 0:
                    stdscr.clear()
                    selected = 0
                    error = "Not Implemented yet"
                if selected == 1:
                    stdscr.clear()
                    selected = 0
                    error = "Not Implemented yet"
                if selected == 2:
                    stdscr.clear()
                    selected = 0
                    error = "Not Implemented yet"

        # clear screen to avoid overlap
        stdscr.clear()


# Libvirt

def getDomains():
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    domains = conn.listAllDomains(0)

    nameslist = []
    for domain in domains:
        nameslist.append(domain.name())

    conn.close
    return nameslist


def getDomainActive(domName):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    dom = None
    try:
        dom = conn.lookupByName(domName)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    flag = dom.isActive()

    conn.close()

    return flag  # return the state of the VM 1 means active/running 0 means inactive/stopped


def startDomain(domName):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    dom = None
    try:
        dom = conn.lookupByName(domName)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    dom.create()

    conn.close()


def stopDomain(domName):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    dom = None
    try:
        dom = conn.lookupByName(domName)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)

    dom.destroy()

    conn.close()


if __name__ == '__main__':
    exit(main())
