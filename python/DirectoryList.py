# -*- coding: utf-8 -*-

from PySide import QtCore


class DirectoryModel(QtCore.QAbstractListModel):
    def __init__(self, directoryListItems):
        QtCore.QAbstractListModel.__init__(self)
        self._directoryListItems = directoryListItems
        self.setRoleNames({0: 'directoryItem'})

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._directoryListItems)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self._directoryListItems[index.row()]


class DirectoryListWrapper(QtCore.QObject):
    def __init__(self, directoryname):
        QtCore.QObject.__init__(self)
        self.__directoryname = directoryname

    def _directoryName(self):
        return self.__directoryname

    clicked = QtCore.Signal()
    directoryname = QtCore.Property(unicode, _directoryName, notify=clicked)


class DirectoryController(QtCore.QObject):
    directoryClicked = QtCore.Signal(str)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, model, wrapper):
        global view, __doc__
        self.directoryClicked.emit(str(wrapper._directoryName()))
