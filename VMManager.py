import libvirt
import sys
import subprocess
import glob
import os

class VMManager(object):
    # The Path of the new Images
    pathOfServerDirectory = "/pathToServer" # username@remote_host:/home/username/dir1 place_to_sync_on_local_machine
    # The Path of the read only Images
    pathOfCleanImages = "/vlab/domains"
    # The Path of the Images wich are currently in use
    pathOfWorkingImages = "/vlab/working"
    # The Path of the script that runs on sync
    pathOfScript = "./vlab/synced/script.sh"

    def __init__(self):
        # start the connection to Libvirt
        self.path ="qemu:///system"
        self.conn = None
        try:
            self.conn = libvirt.open(self.path)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

        #catch prints libvirt
        #libvirt.registerErrorHandler(f=VMManager.libvirt_callback, ctx=None)

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
            raise

        dom.destroy()

    def defineDomain(self,xml):
        try:
            self.conn.defineXMLFlags(xml, 0)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

    def undefineDomain(self,domName):
        dom = None
        try:
            dom = self.conn.lookupByName(domName)
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            raise

        dom.undefineFlags(libvirt.VIR_DOMAIN_UNDEFINE_NVRAM)


    # FILE MANAGMENT

    def checkimage(self,vmname):
        return os.path.isfile(VMManager.pathOfWorkingImages+"/"+vmname+".qcow2")

    def resetImg(self, vmname):
        #creatingWorkingdirectory if not exists
        subprocess.check_output(["mkdir","-p", VMManager.pathOfWorkingImages], stderr=subprocess.STDOUT)


        #search for path of old file
        for path in glob.glob(VMManager.pathOfWorkingImages+"/**/"+vmname+".qcow2",recursive=True):
            # delte old file
            subprocess.check_output(["rm", path], stderr=subprocess.STDOUT)

        #search for path of new file
        newFilePath = glob.glob(VMManager.pathOfCleanImages+"/**/"+vmname+".qcow2")[1]


        # create new subimg
        subprocess.check_output(
            ["qemu-img", "create", "-f", "qcow2", "-F", "qcow2", "-b", newFilePath,
             VMManager.pathOfWorkingImages + "/" + vmname + ".qcow2"], stderr=subprocess.STDOUT)

    def syncImgs(self):
        # sync all files of the server into the local read only directory
        try:
            subprocess.check_output(["rsync", "-a", VMManager.pathOfServerDirectory + "/", VMManager.pathOfCleanImages], stderr=subprocess.STDOUT)
        except Exception as e:
            pass

    def redefineAllImages(self):

        #undefine all domains
        for domName in self.getDomains():
            self.undefineDomain(domName)

        #delete all working images
        try:
            subprocess.check_output(["rm",VMManager.pathOfWorkingImages], stderr=subprocess.STDOUT)
        except Exception as e:
            pass

        # run shellscript to generate xml
        for pathOfFile in glob.glob(VMManager.pathOfCleanImages + "/**/*.xml.TEMPLATE", recursive=True):
            pathOfDir = os.path.dirname(pathOfFile)
            try:
                subprocess.check_output([VMManager.pathOfScript, pathOfDir], stderr=subprocess.STDOUT)
            except Exception as e:
                pass

        xmlList = []
        # getting all xml files
        for xmlpath in glob.glob(VMManager.pathOfCleanImages + "/**/*.xml", recursive=True):
            xml_file = open(xmlpath, "r")

            # read whole file to a string
            xmlList.append(xml_file.read())

            # close file
            xml_file.close()

        # redifining all VMS from the XML Files
        for xml in xmlList:
            if xml:
                self.defineDomain(xml)


    # Removing Libvirt Console out
    #def libvirt_callback(userdata, err):
    #    pass


