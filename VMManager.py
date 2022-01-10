import libvirt
import sys

class VMManager:

    def __init__(self):
        self.path ="qemu:///system"
        self.conn = None
        try:
            self.conn = libvirt.open(self.path)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise


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