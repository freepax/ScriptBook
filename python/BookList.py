# -*- coding: utf-8 -*-

from PySide import QtCore


class BookModel(QtCore.QAbstractListModel):
    def __init__(self, bookListItems):
        QtCore.QAbstractListModel.__init__(self)
        self._bookListItems = bookListItems
        self.setRoleNames({0: 'bookItem'})

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._bookListItems)

    def data(self, index, role):
        if index.isValid() and role == 0:
            return self._bookListItems[index.row()]


class BookListWrapper(QtCore.QObject):
    def __init__(self, entry, name, chapters):
        QtCore.QObject.__init__(self)
        self.__entry = entry
        self.__name = name
        self.__chapters = chapters

    def _entry(self):
        return str(self.__entry)

    def _name(self):
        return self.__name

    def _chapters(self):
        return str(self.__chapters)

    clicked = QtCore.Signal()

    entry = QtCore.Property(unicode, _entry, notify=clicked)
    name = QtCore.Property(unicode, _name, notify=clicked)
    chapters = QtCore.Property(unicode, _chapters, notify=clicked)


class BookController(QtCore.QObject):
    bookClicked = QtCore.Signal(int)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, model, wrapper):
        global view, __doc__
        print "BookController::clicked: entry", wrapper._entry(), "name", wrapper._name(), "chapters", wrapper._chapters()
        self.bookClicked.emit(int(wrapper._entry()))
