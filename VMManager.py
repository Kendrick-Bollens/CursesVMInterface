import libvirt
import sys
import subprocess

class VMManager:
    # The Path of the new Images
    serverPath = "/home/kenny/Desktop/NewVLAB"
    # The Path of the read only Images
    cleanPath = "/home/kenny/Desktop/VLAB"
    # The Path of the Images wich are currently in use
    workingPath = cleanPath + "/working"

    def __init__(self):
        self.path ="qemu:///system"
        self.conn = None
        try:
            self.conn = libvirt.open(self.path)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

    #LIBVIRT

    def restartConnection(self):

        self.conn.close()
        try:
            conn = libvirt.open(self.path)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

    def getDomains(self):

        domains = self.conn.listAllDomains(0)
        nameslist = []
        for domain in domains:
            nameslist.append(domain.name())
        return nameslist


    def getDomainActive(self,domName):

        dom = None
        try:
            dom = self.conn.lookupByName(domName)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

        flag = dom.isActive()
        return flag  # return the state of the VM 1 means active/running 0 means inactive/stopped


    def getFirstActiveDomain(self):
        domains = self.getDomains()
        for dom in domains:
            if self.getDomainActive(dom) == 1:
                return dom
        return None


    def startDomain(self,domName):

        dom = None
        try:
            dom = self.conn.lookupByName(domName)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

        dom.create()


    def restartDomain(self,domName):

        dom = None
        try:
            dom = self.conn.lookupByName(domName)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

        dom.reboot()


    def stopDomain(self,domName):

        dom = None
        try:
            dom = self.conn.lookupByName(domName)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

        dom.shutdown()


    def forceStopDomain(self,domName):

        dom = None
        try:
            dom = self.conn.lookupByName(domName)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            exit(1)

        dom.destroy()

    # FILE MANAGMENT

    def resetImg(self, vmname):
        #creatingWorkingdirectory if not exists
        subprocess.check_output(["mkdir","-p",VMManager.workingPath])
        # delte old file
        subprocess.check_output(["rm", VMManager.workingPath + "/" + vmname + ".qcow2"])
        # create new subimg
        subprocess.check_output(
            ["qemu-img", "create", "-f", "qcow2", "-F", "qcow2", "-b", VMManager.cleanPath + "/" + vmname + ".qcow2",
             VMManager.workingPath + "/" + vmname + ".qcow2"])

    def syncImgs(self):
        #sync all files of the server into the local read only directory
        subprocess.check_output(["rsync", "-a", VMManager.serverPath + "/", VMManager.cleanPath])