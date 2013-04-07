# -*- coding: utf-8 -*-

from PySide import QtCore


class FileModel(QtCore.QAbstractListModel):
    def __init__(self, fileListItems):
        QtCore.QAbstractListModel.__init__(self)
        self._fileListItems = fileListItems
        self.setRoleNames({0: 'fileItem'})

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._fileListItems)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self._fileListItems[index.row()]


class FileListWrapper(QtCore.QObject):
    def __init__(self, filename):
        QtCore.QObject.__init__(self)
        self.__filename = filename

    def _fileName(self):
        return self.__filename

    clicked = QtCore.Signal()
    filename = QtCore.Property(unicode, _fileName, notify=clicked)


class FileController(QtCore.QObject):
    fileClicked = QtCore.Signal(str)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, model, wrapper):
        global view, __doc__
        self.fileClicked.emit(str(wrapper._fileName()))
