# -*- coding: utf-8 -*-

from PySide import QtCore


class DocumentModel(QtCore.QAbstractListModel):
    def __init__(self, documentListItems):
        QtCore.QAbstractListModel.__init__(self)
        self._documentListItems = documentListItems
        self.setRoleNames({0: 'documentItem'})

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._documentListItems)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self._documentListItems[index.row()]


class DocumentListWrapper(QtCore.QObject):
    def __init__(self, entry, filesize, filename):
        QtCore.QObject.__init__(self)
        self.__entry = entry
        self.__filename = filename
        self.__filesize = filesize

    def _entry(self):
        return self.__entry

    def _fileName(self):
        return self.__filename

    def _fileSize(self):
        return self.__filesize

    clicked = QtCore.Signal()
    entry = QtCore.Property(unicode, _entry, notify=clicked)
    filesize = QtCore.Property(unicode, _fileSize, notify=clicked)
    filename = QtCore.Property(unicode, _fileName, notify=clicked)


class DocumentController(QtCore.QObject):
    documentClicked = QtCore.Signal(str)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, model, wrapper):
        global view, __doc__
        self.documentClicked.emit(str(wrapper._fileName()))
