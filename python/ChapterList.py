# -*- coding: utf-8 -*-

from PySide import QtCore


class ChapterModel(QtCore.QAbstractListModel):
    def __init__(self, chapterListItems):
        QtCore.QAbstractListModel.__init__(self)
        self._chapterListItems = chapterListItems
        self.setRoleNames({0: 'chapterItem'})

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._chapterListItems)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self._chapterListItems[index.row()]


class ChapterListWrapper(QtCore.QObject):
    def __init__(self, no, verses, text):
        QtCore.QObject.__init__(self)
        self.__no = no
        self.__verses = verses
        self.__text = text

    def _no(self):
        return str(self.__no)

    def _verses(self):
        return self.__verses

    def _text(self):
        return self.__text

    clicked = QtCore.Signal()

    no = QtCore.Property(unicode, _no, notify=clicked)
    verses = QtCore.Property(unicode, _verses, notify=clicked)
    text = QtCore.Property(unicode, _text, notify=clicked)


class ChapterController(QtCore.QObject):
    chapterClicked = QtCore.Signal(int)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, model, wrapper):
        global view, __doc__
        print "ChapterController::clicked: no", wrapper._no(), "verses", wrapper._verses()
        self.chapterClicked.emit(int(wrapper._no()))
