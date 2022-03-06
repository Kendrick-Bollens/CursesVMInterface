# CursesVmInterface
This is a school project to combine the curses interface with the libvirt api to controll VMs via a simple curses Interface.
The interface is locked down for simple use to not toy with the pc.

## How to use
1. install python3
2. install the libvirt-package package for python
3. download this software 
4. run the start.py or put it inside a cron job

## What to modify
inside the VMManganer.py there are 4 paths 

- The first is for the Server from wich the pc gets its updates
- The second is for the path of the untouched images
- The third is for the images wich are used for working
- The last is a Script wich is used for automatic editing the XMLs.