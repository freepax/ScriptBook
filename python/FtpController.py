# -*- coding: utf-8 -*-

from PySide import QtCore

class FtpController(QtCore.QObject):
    _host = str("")
    _port = str("")

    def __init__(self, parent = None):
        super(FtpController, self).__init__(parent)

    @QtCore.Slot(result=str)
    def getHost(self):
        return self._host

    def setHost(self, host):
        self._host = host

    @QtCore.Slot(result=str)
    def getPort(self):
        return self._port

    def setPort(self, port):
        self._port = port


    onHostChanged = QtCore.Signal(str)
    host = QtCore.Property(str, getHost, setHost, notify=onHostChanged)

    onPortChanged = QtCore.Signal(str)
    port = QtCore.Property(str, getPort, setPort, notify=onPortChanged)

    connectSignal = QtCore.Signal(str, str)
    disconnectSignal = QtCore.Signal()
    cancelSignal = QtCore.Signal()


