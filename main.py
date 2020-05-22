from main_ui import *
import re
from ipaddress import *
import datetime
import ctypes
import sys
import traceback
import logging
import os

try:
    from Qt import QtCore, QtWidgets
    import PyQt5
except ImportError:
    os.system('python -m pip install --upgrade pip  ')
    os.system('python -m pip install --upgrade PyQt5  ')
    os.system('python -m pip install --upgrade qt.py  ')

    from Qt import QtCore, QtWidgets


user32 = ctypes.windll.user32
errorsFoundList = []
ipAddressDuplicatedList = []
ipAddressList = []
createdObjectsCount = 0
hostNamesList = []

#============ ERRORS ====================
# basic logger functionality
log = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
log.addHandler(handler)


def show_exception_box(log_msg):
    """Checks if a QApplication instance is available and shows a messagebox with the exception message.
    If unavailable (non-console application), log an additional notice.
    """
    if QtWidgets.QApplication.instance() is not None:
        errorbox = QtWidgets.QMessageBox()
        errorbox.setText("Oops. An unexpected error occured:\n{0}".format(log_msg))
        errorbox.exec_()
    else:
        log.debug("No QApplication instance available.")


class UncaughtHook(QtCore.QObject):
    _exception_caught = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])
            log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            self._exception_caught.emit(log_msg)


# create a global instance of our class to register the hook
qt_exception_hook = UncaughtHook()

#============ PROGRAM ===================


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButtonConvert.clicked.connect(self.convert)
        self.pushButtonExample.clicked.connect(self.example)
        # self.radioButtonFortigate.setChecked(True)
        self.radioButtonCisco.setChecked(True)
        self.checkBoxCreateGroup.clicked.connect(self.group)
        self.checkBoxIsNBF.clicked.connect(self.virtual)
        self.lineEditGroupName.setEnabled(False)
        self.radioButtonNorth.setEnabled(False)
        self.radioButtonSouth.setEnabled(False)

    # -----------------------------------COMMON---------------------------------------
    def group(self):
        if self.checkBoxCreateGroup.isChecked():
            self.lineEditGroupName.setEnabled(True)
        else:
            self.lineEditGroupName.setEnabled(False)

    def virtual(self):
        if self.checkBoxIsNBF.isChecked():
            self.radioButtonNorth.setEnabled(True)
            self.radioButtonSouth.setEnabled(True)
            self.labelResultsErrors.setText("Please select a interface")
        else:
            self.radioButtonNorth.setEnabled(False)
            self.radioButtonSouth.setEnabled(False)
            self.labelResultsErrors.setText("")
    def convert(self):
        del errorsFoundList[:]
        del ipAddressDuplicatedList[:]
        del ipAddressList[:]
        del hostNamesList[:]
        errors = False
        groupText = self.lineEditGroupName.text()
        commentText = self.lineEditComment.text()
        errorText = ""
        if self.checkBoxCreateGroup.isChecked():
            if groupText == "":
                errorText += "Please add group name \n"
                errors = True

        if commentText == "" and self.radioButtonFortigate.isChecked():
            errorText += "Please add comment \n"
            errors = True

        if errors:
            self.labelResultsErrors.setText(errorText)
        else:
            self.labelResultsErrors.setText("")
            if self.radioButtonFortigate.isChecked():
                self.createNewObjects()
            elif self.radioButtonCisco:
                self.createNewObjectsCisco()

    def example(self):
        t = """EXAMPLES:
        1.1.1.1
        2.2.2.2
        10.20.30.40
        255.244.233.266
        10.0.0.0/8

        EXAMPLES: With custom names
        1.1.1.1 host1
        2.2.2.2 host2 
        10.20.30.40 host3 
        255.244.233.266 hostwitherror
        10.0.0.0/8 network-10
        """
        errorbox = QtWidgets.QMessageBox()
        errorbox.setText(t)
        errorbox.exec_()


    def createComment(self):
        today = datetime.date.today()
        o = self.lineEditComment.text()
        t = str(o) + "-" + str(today.strftime('%d%B%Y'))
        self.plainTextEditComment.appendPlainText(t)

    def optCreationOfHost_NetObjects_CustomNames(self):

        clearText = self.plainTextEditOriginal.toPlainText()
        listOfTexts = []
        lVarIpObjects = []
        for line in clearText.splitlines():
            lineText = re.findall(r"\S+", line)
            if len(lineText) > 0:
                listOfTexts.append(lineText)
        list1 = []
        list2 = []
        for oneLine in listOfTexts:
            if self.createIpObjects(oneLine[0]) != "error":
                list1.append(self.createIpObjects(oneLine[0]))
                try:
                    list2.append(oneLine[1])
                except:
                    list2.append("'Insert text here'")
                
            # lVarIpObjects.append([createIpObjects(oneLine[0]),oneLine[1]])

        lVarIpObjects.append([list1, list2])
        return lVarIpObjects

    def removeWhiteSpaces(self,data):

        try:
            x = data.index(" ")

            if data[x + 1].isnumeric():
                data = re.sub(r"\s+", "/", data, flags=re.UNICODE)
                return data
            else:
                data = ''.join(data.split())
                return data
        #except Exception as e:
        except:
            data = re.sub(r"\s+", "", data, flags=re.UNICODE)
            return data.rstrip()

    def createIpObjects(self,address):

        try:
            if address and address.isspace():
                network = ip_network(u'' + address)
                return network
            else:
                address = self.removeWhiteSpaces(address)
                network = ip_network(u'' + address)
                return network
        except ValueError:
            error = sys.exc_info()[1]
            errorsFoundList.append(str(error))
            var = "error"
            return var
            pass

    def isNotEmpty(self,s):

        return bool(s and s.strip())

    def showResults(self,fullText, counter):

        ft = fullText
        cc = counter
        errors = ""
        dupli = ""
        resu = ""
        self.plainTextEditResult.clear()
        if ft:
            if len(errorsFoundList) > 0:
                self.plainTextEditResult.appendPlainText("\n".join(map(str, errorsFoundList)))
                self.plainTextEditResult.appendPlainText("\n")
                self.plainTextEditResult.appendPlainText("------------" + str(len(errorsFoundList)) + " errors found--------------")
                errors = "Errors found: " + str(len(errorsFoundList))
                self.plainTextEditResult.appendPlainText("\n")
            if len(ipAddressDuplicatedList) > 0:
                self.plainTextEditResult.appendPlainText("\n".join(map(str, ipAddressDuplicatedList)))
                self.plainTextEditResult.appendPlainText("\n")
                self.plainTextEditResult.appendPlainText("------------" + str(len(ipAddressDuplicatedList)) + " duplicated found--------------")
                dupli = "Duplicated found: " + str(len(ipAddressDuplicatedList))
                self.plainTextEditResult.appendPlainText("\n")
            # app.setTextArea("t2","\n".join(map(str,fullScript)))
            self.plainTextEditResult.appendPlainText(ft)
            self.plainTextEditResult.appendPlainText("\n")
            # oapp.setTextArea("t2","------------Objects created:" + str(cc) + "--------------")
            resu = "Objects created:" + str(cc) + ". "
            self.labelResults.setText("Results: " + " | " + resu + " | " + dupli + " | " + errors)

    # -------------------------------------Fortigate---------------------------------------
    def createNewObjects(self):

        useCustomNames = self.checkBoxCustomNames.isChecked()
        createGroupWEObj = self.checkBoxCreateGroup.isChecked()

        finalScript = []

        if useCustomNames:
            oList = self.optCreationOfHost_NetObjects_CustomNames()
            for x in oList:
                for x in oList[0][0]:  # remove duplicated
                    if oList[0][0].count(x) > 1:
                        w = oList[0][0].index(x)
                        z = oList[0][1][w]
                        ipAddressDuplicatedList.append(["Address: " + str(x.with_prefixlen), "Object name:" + z])
                        oList[0][0].remove(x)
                        oList[0][1].remove(z)

                for x in oList[0][0]:  # create script
                    w = oList[0][0].index(x)
                    nameO = oList[0][1][w]
                    ipO = oList[0][0][w]
                    parcialScript = self.createScript(nameO, ipO)
                    finalScript.append(parcialScript)
                    hostNamesList.append("\"" + nameO + "\"")
                cc = len(oList)
            t = "\n".join(map(str, finalScript))
            if createGroupWEObj:
                t = t + self.createGroup(hostNamesList)
            self.showResults(t, len(ipAddressList))
        else:
            ft = self.plainTextEditOriginal.toPlainText()
            for x in ft.splitlines():
                ipobject = self.createIpObjects(x)
                if ipobject != "error":
                    if ipobject not in ipAddressList:
                        ipAddressList.append(ipobject)
                    else:
                        ipAddressDuplicatedList.append(ipobject)
            for x in ipAddressList:
                virtual = self.checkBoxIsNBF.isChecked()
                if virtual:  # Different naming convention
                    if not self.radioButtonNorth.isChecked() and not self.radioButtonSouth.isChecked():
                        self.radioButtonNorth.setChecked(True)
                    if self.radioButtonNorth.isChecked():
                        if x.prefixlen == 32:  # External or public address
                            objName = "External Server " + str(x.network_address)
                        else:
                            objName = "External Network " + str(x.network_address) + "m" + str(x.prefixlen)
                    if self.radioButtonSouth.isChecked():
                        if x.prefixlen == 32:
                            objName = "Internal Server " + str(x.network_address)
                        else:
                            objName = "Internal Network " + str(x.network_address) + "m" + str(x.prefixlen)

                else:
                    if x.prefixlen == 32:
                        objName = "Host_" + str(x.network_address)
                    else:
                        objName = "Network_" + str(x.network_address) + "m" + str(x.prefixlen)

                finalScript.append(self.createScript(objName, x))
                hostNamesList.append("\"" + objName + "\"")
            t = "\n".join(map(str, finalScript))
            if createGroupWEObj:
                t = t + self.createGroup(hostNamesList)
            self.showResults(t, len(ipAddressList))

    def createScript(self,hostName, ipObject):
        comm = self.lineEditComment.text()
        virtual = self.checkBoxIsNBF.isChecked()
        if virtual:
            if self.radioButtonSouth.isChecked():
                virtualInt = "South"
            elif self.radioButtonNorth.isChecked():
                virtualInt = "North"
            fs = """config firewall address
        edit \"{objNamex}\"
            set associated-interface {virtualIntx}
            set comment "{commentx}"
            set subnet {ipObjectx}
        next
    end""".format(objNamex=hostName, commentx=comm, ipObjectx=str(ipObject.with_netmask).replace('/', ' '),
                  virtualIntx=virtualInt)
        else:  # if not
            fs = """config firewall address
        edit \"{objNamex}\"
            set comment "{commentx}"
            set subnet {ipObjectx}
        next
    end""".format(objNamex=hostName, commentx=comm, ipObjectx=str(ipObject.with_netmask).replace('/', ' '))
        return fs

    def createGroup(self,hostNetObjects):
        comm = self.lineEditComment.text()
        gName = self.lineEditGroupName.text()

        fl = ""
        for x in hostNetObjects:
            fl = fl + " " + x
            pass
        ft = """
    config firewall addrgrp
        edit \"{gName}\"
            set comment '{userComment}'
            set member {fl}
            set visibility enable
        next
    end""".format(gName=gName, userComment=comm, fl=fl)
        return ft

    # ---------------------------------------CISCO------------------------------------------
    def createNewObjectsCisco(self):  # CISCO Scripts
        useCustomNames = self.checkBoxCustomNames.isChecked()
        createGroupWEObj = self.checkBoxCreateGroup.isChecked()
        finalScript = []
        if useCustomNames:
            oList = self.optCreationOfHost_NetObjects_CustomNames()
            for x in oList:
                for x in oList[0][0]:  # remove duplicated
                    if oList[0][0].count(x) > 1:
                        w = oList[0][0].index(x)
                        z = oList[0][1][w]
                        ipAddressDuplicatedList.append(["Address: " + str(x.with_prefixlen), "Object name:" + z])
                        oList[0][0].remove(x)
                        oList[0][1].remove(z)

                for x in oList[0][0]:  # create script
                    w = oList[0][0].index(x)
                    nameO = oList[0][1][w]
                    ipO = oList[0][0][w]
                    parcialScript = self.createScriptCisco(nameO, ipO)
                    finalScript.append(parcialScript)
                    hostNamesList.append("\"" + nameO + "\"")
                cc = len(oList)
        else:
            ft = self.plainTextEditOriginal.toPlainText()
            for x in ft.splitlines():
                ipobject = self.createIpObjects(x)
                if ipobject != "error":
                    if ipobject not in ipAddressList:
                        ipAddressList.append(ipobject)
                    else:
                        ipAddressDuplicatedList.append(ipobject)
            for x in ipAddressList:
                nameO = str(x.network_address)
                parcialScript = self.createScriptCisco(nameO, x)
                finalScript.append(parcialScript)
                hostNamesList.append("\"" + nameO + "\"")
            cc = len(ipAddressList)
        t = "\n".join(map(str, finalScript))
        if createGroupWEObj:
            t = t + "\n" + "--------------- Group ----------------" + "\n" + self.createGroupCisco(hostNamesList)
        self.showResults(t, len(ipAddressList))

    def createScriptCisco(self,hostName, ipObject):
        #comm = self.lineEditComment.text()
        if ipObject.prefixlen == 32:
            fs = """object network {objNamex}
     host {ipObjectx}
    """.format(objNamex=hostName, ipObjectx=str(ipObject.network_address))
        else:
            fs = """object network {objNamex}
     subnet {ipObjectx}
    """.format(objNamex=hostName, ipObjectx=str(ipObject.with_netmask).replace('/', ' '))
        return fs

    def createGroupCisco(self,hostNetObjects):
        gName = self.lineEditGroupName.text()
        if not gName:
            app.infoBox("Error", "You forgot to add the group name")
            pass
        var1 = "object-group network " + gName + "\n"
        fl = ""
        for x in hostNetObjects:
            fl = fl + " network-object object " + x + "\n"
            pass
        ft = var1 + fl
        return ft



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.setWindowTitle("Firewall object creator - By:Muadiv")
    window.show()

    app.exec_()



