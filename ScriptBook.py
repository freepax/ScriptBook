#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtXml
from PySide import QtDeclarative

sys.path.append('python')
import Document
import BookList
import ChapterList
import VerseList
import DocumentHandler
import DocumentList


class NavigationController(QtCore.QObject):
    buttonClicked = QtCore.Signal(int)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, button):
        #global view, __doc__ #### view ???
        #print "NavigationController::clicked: Button", button
        self.buttonClicked.emit(int(button))


class ScriptBook(QtGui.QStackedWidget):
    def __init__(self, parent=None):
        super(ScriptBook, self).__init__(parent)
        self.document = Document.Document()
        self.handler = DocumentHandler.DocumentHandler()

        ## Set values for the store/restore settings system
        QtCore.QCoreApplication.setOrganizationName("EMR")
        QtCore.QCoreApplication.setOrganizationDomain("code.rutger.no")
        QtCore.QCoreApplication.setApplicationName("ScriptBook")

        ## The button controller
        self.buttonController = NavigationController()
        self.buttonController.buttonClicked.connect(self.buttonClicked)

        ## Set up UI components
        self.setupUI()


    def setupUI(self):
        ## The document view, controller and  model
        self.documentView = QtDeclarative.QDeclarativeView()
        self.documentView.setWindowTitle('Documents')
        self.documentView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.documentController = DocumentList.DocumentController()
        self.documentController.documentClicked.connect(self.documentClicked)
        self.documentView.rootContext().setContextProperty('controller', self.documentController)
        self.documentView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.documentList = DocumentList.DocumentModel([])
        self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)
        self.documentView.setSource(QtCore.QUrl('qml/DocumentListModel.qml'))

        ## The book view, controller and  model
        self.bookView = QtDeclarative.QDeclarativeView()
        self.bookView.setWindowTitle('Books')
        self.bookView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.bookController = BookList.BookController()
        self.bookController.bookClicked.connect(self.bookClicked)
        self.bookView.rootContext().setContextProperty('controller', self.bookController)
        self.bookView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.bookList = BookList.BookModel([])
        self.bookView.rootContext().setContextProperty('bookListModel', self.bookList)
        self.bookView.setSource(QtCore.QUrl('qml/BookListModel.qml'))

        ## The chapter view, controller and  model
        self.chapterView = QtDeclarative.QDeclarativeView()
        self.chapterView.setWindowTitle('Chapter')
        self.chapterView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.chapterController = ChapterList.ChapterController()
        self.chapterController.chapterClicked.connect(self.chapterClicked)
        self.chapterView.rootContext().setContextProperty('controller', self.chapterController)
        self.chapterView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.chapterList = ChapterList.ChapterModel([])
        self.chapterView.rootContext().setContextProperty('chapterListModel', self.chapterList)
        self.chapterView.setSource(QtCore.QUrl('qml/ChapterListModel.qml'))

        ## The chapter view, controller and  model
        self.verseView = QtDeclarative.QDeclarativeView()
        self.verseView.setWindowTitle('Chapter')
        self.verseView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.verseController = VerseList.VerseController()
        self.verseController.verseClicked.connect(self.verseClicked)
        self.verseView.rootContext().setContextProperty('controller', self.verseController)
        self.verseView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.verseList = VerseList.VerseModel([])
        self.verseView.rootContext().setContextProperty('verseListModel', self.verseList)
        self.verseView.setSource(QtCore.QUrl('qml/VerseListModel.qml'))

        ## Add the book, chapter and verse view's
        self.addWidget(self.documentView)
        self.addWidget(self.bookView)
        self.addWidget(self.chapterView)
        self.addWidget(self.verseView)

        ## Set window title, set geometry and show
        self.setWindowTitle('ScriptBook')
        self.setGeometry(400, 200, 300, 450)
        self.show()

        ## Load settings
        self.loadSettings()

        self.loadDocuments()


    def loadDocuments(self):
        documentListItems = []        
        dirFilter = []
        dirFilter.append('*.xml')
        directory = QtCore.QDir()
        dirList = directory.entryList(dirFilter)
        if len(dirList) > 0:
            for fileName in dirList:
                documentListItems.append(DocumentList.DocumentListWrapper(fileName))

        self.documentList = DocumentList.DocumentModel(documentListItems)
        self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)



    def loadSettings(self):
        ## Read the settings
        settings = QtCore.QSettings()
        document = settings.value("ScriptBook/document")
        book = settings.value("ScriptBook/book")
        chapter = settings.value("ScriptBook/chapter")
        vers = settings.value("ScriptBook/vers")

        ## Check if we can load something
        if document != None:
            print 'document', document
            if self.openFile(document) == True:
                if chapter != None and book != None:
                    if self.loadBook(int(book)) == True and self.loadChapter(int(chapter)) == True:
                        self.setCurrentWidget(self.verseView)
                elif book != None and self.loadBook(int(book)) == True:
                    self.setCurrentWidget(self.chapterView)


    def loadBook(self, book):
        try:
            chapterListItems = []
            books = self.document.books()
            for b in books:
                if int(b.document_entry) == int(book):
                    self.book = b
                    chapters = self.book.chap()
                    for c in chapters:
                        chapterListItems.append(ChapterList.ChapterListWrapper(c.no, c.verses, c.vers()[0].text))
                    break

            self.chapterList = ChapterList.ChapterModel(chapterListItems)
            self.chapterView.rootContext().setContextProperty('chapterListModel', self.chapterList)
            return True
        except:
            return False


    def documentClicked(self, document):
        print 'documentClicked', document
        if self.openFile(document) == True:
            self.setCurrentWidget(self.bookView)


    def bookClicked(self, book):
        if self.loadBook(book) == True:
            self.setCurrentWidget(self.chapterView)
            self.setWindowTitle(str("ScriptBook %s" % self.book.name))


    def loadChapter(self, chapter):
        try:
            verseListItems = []
            chapters = self.book.chap()
            for c in chapters:
                if int(c.no) == int(chapter):
                    v = c.vers()
                    for i in v:
                        textstring = str("%s %s" % (str(i.number), i.text))
                        verseListItems.append(VerseList.VerseListWrapper(int(i.number), textstring))
                        #verseListItems.append(VerseList.VerseListWrapper(int(i.number), str(i.text)))
                    break

            self.verseList = VerseList.VerseModel(verseListItems)
            self.verseView.rootContext().setContextProperty('verseListModel', self.verseList)
            return True
        except:
            print 'loadChapter failed'
            return False


    def chapterClicked(self, chapter):
        if self.loadChapter(chapter) == True:
            self.setCurrentWidget(self.verseView)

            ## Write bookmark to settings
            settings = QtCore.QSettings()
            settings.setValue("ScriptBook/chapter", chapter)
            settings.setValue("ScriptBook/book", self.book.document_entry)


    def verseClicked(self, verse):
        ## Write the verse to settings (needed ?)
        settings = QtCore.QSettings()
        settings.setValue("ScriptBook/verse", verse)

        ## Shoud give pop up options here
        ## 1. Save bookmark
        ## 2. Save note
        ## 3. Higlight (set different font and background color)


    def buttonClicked(self, button):
        if button == 0:
            self.loadDocuments()
            self.setCurrentWidget(self.documentView)
        elif button == 1:
            self.setCurrentWidget(self.bookView)
        elif button == 2:
            self.setCurrentWidget(self.chapterView)
        elif button == 3:
            print 'ScriptBook::buttonClicked Tools', button


    def openFile(self, filename):
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "ScriptBook", "Cannot read file \n%s:\n." % filename)
            return False

        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(self.handler)
        reader.setErrorHandler(self.handler)

        xmlInputSource = QtXml.QXmlInputSource(file)

        if reader.parse(xmlInputSource) == False:
            QtGui.QMessageBox.warning(self, "ScriptBook", "Cannot read file \n%s:\n." % filename)
            return False

        # document stuff here
        self.document = self.handler.document

        bookListItems = []

        books = self.document.books()
        for b in books:
            bookListItems.append(BookList.BookListWrapper(b.document_entry, b.name, b.chapters))

        self.bookList = BookList.BookModel(bookListItems)
        self.bookView.rootContext().setContextProperty('bookListModel', self.bookList)

        self.setWindowTitle(str(("ScriptBook %s" % self.document.description)))

        ## Write the filename
        settings = QtCore.QSettings()
        settings.setValue("ScriptBook/document", filename)

        return True


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    scriptBook = ScriptBook()
    #scriptBook.openFile('script-book.xml')
    #scriptBook.openFile('king-james-english.xml')

    sys.exit(app.exec_())
