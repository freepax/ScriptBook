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



class NavigationController(QtCore.QObject):
    buttonClicked = QtCore.Signal(int)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, button):
        #global view, __doc__ #### view ???
        #print "NavigationController::clicked: Button", button
        self.buttonClicked.emit(int(button))


class DocumentHandler(QtXml.QXmlDefaultHandler):
    def __init__(self):
        super(DocumentHandler, self).__init__()

        self.document = Document.Document()
        self.book = Document.Book()
        self.chapter = Document.Chapter()
        #self.comment = Document.Comment()
        self.vers = Document.Vers()

        self.errorStr = ''
        self.item = None
        self.documentStartTag = False


    def startElement(self, namespaceURI, localName, qName, attributes):
        if not self.documentStartTag and qName != 'document':
            self.errorStr = "The file is not an ScriptBook file."
            return False

        if qName == 'document':
            self.document = Document.Document()
            self.document.description = attributes.value('description')
            self.document.language = attributes.value('language')
            self.document.entries = int(attributes.value('entries'))
            self.documentStartTag = True

        elif qName == 'book':
            self.book.name = attributes.value('name')
            self.book.document_entry = int(attributes.value('document-entry'))
            self.book.chapters = int(attributes.value('chapters'))

        elif qName == 'chapter':
            self.chapter.no = attributes.value('no')
            self.chapter.verses = attributes.value('verses')

        #elif qName == 'comment':
            #print "DEBUG COMMENT", attributes.value('text')

        elif qName == 'vers':
            self.vers.number = attributes.value('no')
            self.vers.text = attributes.value('text')

        return True


    def endElement(self, namespaceURI, localName, qName):
        if qName == 'document':
            self.documentStartTag = False

        elif qName == 'book':
            self.document.append(self.book)
            self.book = Document.Book()

        elif qName == 'chapter':
            self.book.append(self.chapter)
            self.chapter = Document.Chapter()

        #elif qName == 'comment':
            #print "END COMMENT"
            #self.comment = Document.Comment()

        elif qName == 'vers':
            self.chapter.appendVers(self.vers)
            self.vers = Document.Vers()

        return True


    def fatalError(self, exception):
        QtGui.QMessageBox.information(self.treeWidget.window(),
                "ScriptBook", "Parse error at line %d, column %d:\n%s" % (exception.lineNumber(), exception.columnNumber(), exception.message()))
        return False

    def errorString(self):
        return self.errorStr

    def createChildItem(self, tagName):
        return childItem


class ScriptBook(QtGui.QStackedWidget):
    def __init__(self, parent=None):
        super(ScriptBook, self).__init__(parent)
        self.document = Document.Document()
        self.handler = DocumentHandler()

        ## Set values for the store/restore settings system
        QtCore.QCoreApplication.setOrganizationName("EMR")
        QtCore.QCoreApplication.setOrganizationDomain("code.rutger.no")
        QtCore.QCoreApplication.setApplicationName("QmlChatClient")

        ## The button controller
        self.buttonController = NavigationController()
        self.buttonController.buttonClicked.connect(self.buttonClicked)

        ## Set up UI components
        self.setupUI()


    def setupUI(self):
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
        self.addWidget(self.bookView)
        self.addWidget(self.chapterView)
        self.addWidget(self.verseView)

        ## Set window title, set geometry and show
        self.setWindowTitle('ScriptBook')
        self.setGeometry(400, 200, 300, 450)
        self.show()

        ## Load settings
        self.loadSettings()


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
    ##################################################################################################

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


    def bookClicked(self, book):
        if self.loadBook(book) == True:
            self.setCurrentWidget(self.chapterView)
            self.setWindowTitle(str("ScriptBook %s" % self.book.name))

            ## Write the book to settings 
            settings = QtCore.QSettings()
            settings.setValue("ScriptBook/book", book)


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

            ## Write the chapter to settings
            settings = QtCore.QSettings()
            settings.setValue("ScriptBook/chapter", chapter)


    def verseClicked(self, verse):
        ## Write the verse to settings
        settings = QtCore.QSettings()
        settings.setValue("ScriptBook/verse", verse)


    def buttonClicked(self, button):
        if button == 0:
            print 'ScriptBook::buttonClicked Docs', button
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
        if reader.parse(xmlInputSource):
            print 'File loaded'

        # document stuff here
        self.document = self.handler.document

        bookListItems = []

        print "Document entries", self.document.entries
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

    sys.exit(app.exec_())
