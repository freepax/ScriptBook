# -*- coding: utf-8 -*-

from PySide import QtCore


class VerseModel(QtCore.QAbstractListModel):
    def __init__(self, verseListItems):
        QtCore.QAbstractListModel.__init__(self)
        self._verseListItems = verseListItems
        self.setRoleNames({0: 'verseItem'})

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._verseListItems)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self._verseListItems[index.row()]


class VerseListWrapper(QtCore.QObject):
    def __init__(self, number, text):
        QtCore.QObject.__init__(self)
        self.__number = number
        self.__text = text

    def _number(self):
        return str(self.__number)

    def _text(self):
        return self.__text

    clicked = QtCore.Signal()

    number = QtCore.Property(unicode, _number, notify=clicked)
    text = QtCore.Property(unicode, _text, notify=clicked)


class VerseController(QtCore.QObject):
    verseClicked = QtCore.Signal(int)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, model, wrapper):
        global view, __doc__
        print "VerseController::clicked: no", wrapper._number(), "text", wrapper._text()
        self.verseClicked.emit(int(wrapper._number()))
