# -*- coding: utf-8 -*-

from PySide import QtCore

class ToolsController(QtCore.QObject):
    toolsClicked = QtCore.Signal(int)

    def __init__(self, parent = None):
        super(ToolsController, self).__init__(parent)
