# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide import QtNetwork


class FtpEntryListController(QtCore.QObject):
    ftpDirectoryListDone = QtCore.Signal()
    ftpChdirDone = QtCore.Signal()
    ftpFileListDone = QtCore.Signal()

    _list = []
    _command = int(-1)
    _commandID = int(0)

    _state = int(-1)

    _host = str("")
    _port = int(0)
    _directory = str(".")


    def __init__(self, parent = None):
        super(FtpEntryListController, self).__init__(parent)

        self.ftp = QtNetwork.QFtp()

        self.ftp.stateChanged.connect(self.stateChanged)
        self.ftp.commandStarted.connect(self.commandStarted)
        self.ftp.commandFinished.connect(self.commandFinished)
        self.ftp.readyRead.connect(self.readyRead)
        self.ftp.listInfo.connect(self.listInfo)


    def list(self):
        return self._list


    def setHostPort(self, host, port):
        if host != str("") and port != int(0):
            self._host = str(host)
            self._port = int(port)


    def hostPortDirectory(self):
        return self._host, self._port, self._directory


    def directoryList(self):
        self._command = 0
        self.ftp.connectToHost(str(self._host), int(self._port))
        self.ftp.login()


    def setDirectory(self, directory):
        self._directory = directory


    def fileList(self):
        self._command = 1
        self.ftp.connectToHost(str(self._host), int(self._port))
        self.ftp.login()


    def disconnectSlot(self):
        self.ftp.close()


    def stateChanged(self, arg):
        #print 'stateChanged', arg, self._command
        if self.ftp.state() == QtNetwork.QFtp.Connected:
            ## Connected - get ftp listing 
            #print 'stateChanged: connected'
            if self._command == 0:
                self._state = int(0)
                self._commandID = self.ftp.cd(self._directory)
            elif self._command == 1:
                self._state = int(0)
                self._commandID = self.ftp.cd(self._directory)
                

        #elif self.ftp.state() == QtNetwork.QFtp.Connecting:
        #    print 'stateChanged: Connecting', self._command

        #elif self.ftp.state() == QtNetwork.QFtp.Closing:
        #    print 'stateChanged: Closing', self._command

        elif self.ftp.state() == QtNetwork.QFtp.Unconnected:
            if self._command == 0:
                self.ftpDirectoryListDone.emit()
            elif self._command == 1:
                self.ftpFileListDone.emit()


    def commandStarted(self, arg):
        if arg == self._commandID:
            self._list = []
            #print 'commandStarted: commandId', self._commandID


    def commandFinished(self, arg):
        if arg == self._commandID:
            #print 'commandFinished: ID match'
            ## Directory list
            if self._command == int(0):
                if self._state == int(0):
                    self._state = 1
                    self._commandID = self.ftp.list()
                elif self._state == int(1):
                    self._state = -1
                    self.disconnectSlot()
                else:
                    self._state = -1
                    self.disconnectSlot()

            ## File list
            elif self._command == int(1):
                if self._state == int(0):
                    self._state = 1
                    self._commandID = self.ftp.list()
                elif self._state == int(1):
                    self._state = -1
                    self.disconnectSlot()
                else:
                    self._state = -1
                    self.disconnectSlot()

            #for f in self.fileList:
            #    self.getFile(f)

            else:
                self.disconnectSlot()


    def readyRead(self):
        print 'readyRead', self.ftp.bytesAvailable(), " content", str(self.ftp.readAll())


    def listInfo(self, info):
        if info.isDir() == True:
            if self._command == int(0):
                #print 'DIRECTORY', info.name()
                self._list.append(info.name())
        elif info.isFile() == True:
            if self._command == int(1):
                filename = info.name()
                if filename.split('.')[1] == 'xml':
                    #print 'XML FILE', info.name()
                    self._list.append(filename)
