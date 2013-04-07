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
import DocumentXmlHandler
import DocumentList
import ToolsController
import FtpController
import FtpEntryListController
import DirectoryList
import FileList


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
        self.handler = DocumentXmlHandler.DocumentXmlHandler()

        ## Set values for the store/restore settings system
        QtCore.QCoreApplication.setOrganizationName("EMR")
        QtCore.QCoreApplication.setOrganizationDomain("code.rutger.no")
        QtCore.QCoreApplication.setApplicationName("ScriptBook")

        ## The button controller
        self.buttonController = NavigationController()
        self.buttonController.buttonClicked.connect(self.buttonClicked)

        ## The tools controller
        self.toolsController = ToolsController.ToolsController()
        self.toolsController.toolsClicked.connect(self.toolsClicked)

        ## The ftp login controller
        self.ftpController = FtpController.FtpController()
        self.ftpController.connectSignal.connect(self.ftpConnect)
        self.ftpController.cancelSignal.connect(self.ftpCancel)

        ## The ftp entry list controller
        self.ftpEntryListController = FtpEntryListController.FtpEntryListController()
        self.ftpEntryListController.ftpDirectoryListDone.connect(self.ftpDirectoryListDone)
        self.ftpEntryListController.ftpFileListDone.connect(self.ftpFileListDone)

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
        self.verseView.setWindowTitle('Verse')
        self.verseView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.verseController = VerseList.VerseController()
        self.verseController.verseClicked.connect(self.verseClicked)
        self.verseView.rootContext().setContextProperty('controller', self.verseController)
        self.verseView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.verseList = VerseList.VerseModel([])
        self.verseView.rootContext().setContextProperty('verseListModel', self.verseList)
        self.verseView.setSource(QtCore.QUrl('qml/VerseListModel.qml'))

        ## The tools view
        self.toolsView = QtDeclarative.QDeclarativeView()
        self.toolsView.setWindowTitle('Tools')
        self.toolsView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.toolsView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.toolsView.rootContext().setContextProperty('toolsController', self.toolsController)
        self.toolsView.setSource(QtCore.QUrl('qml/Tools.qml'))

        ## The ftp login view
        self.ftpLoginView = QtDeclarative.QDeclarativeView()
        self.ftpLoginView.setWindowTitle('Ftp login')
        self.ftpLoginView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.ftpLoginView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.ftpLoginView.rootContext().setContextProperty('ftpController', self.ftpController)
        self.ftpLoginView.setSource(QtCore.QUrl('qml/FtpLogin.qml'))

        ## The ftp directory view
        self.directoryView = QtDeclarative.QDeclarativeView()
        self.directoryView.setWindowTitle('Ftp directories')
        self.directoryView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.directoryController = DirectoryList.DirectoryController()
        self.directoryController.directoryClicked.connect(self.directoryClicked)
        self.directoryView.rootContext().setContextProperty('controller', self.directoryController)
        self.directoryList = DirectoryList.DirectoryModel([])
        self.directoryView.rootContext().setContextProperty('directoryListModel', self.directoryList)
        self.directoryView.rootContext().setContextProperty('ftpController', self.ftpController)
        self.directoryView.setSource(QtCore.QUrl('qml/FtpDirectoryListModel.qml'))


        ## The ftp directory view
        self.fileView = QtDeclarative.QDeclarativeView()
        self.fileView.setWindowTitle('Ftp xml files')
        self.fileView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.fileController = FileList.FileController()
        self.fileController.fileClicked.connect(self.fileClicked)
        self.fileView.rootContext().setContextProperty('controller', self.fileController)
        self.fileList = FileList.FileModel([])
        self.fileView.rootContext().setContextProperty('fileListModel', self.fileList)
        self.fileView.rootContext().setContextProperty('ftpController', self.ftpController)
        self.fileView.setSource(QtCore.QUrl('qml/FtpFileListModel.qml'))


        ## Add the book, chapter and verse view's
        self.addWidget(self.documentView)
        self.addWidget(self.bookView)
        self.addWidget(self.chapterView)
        self.addWidget(self.verseView)
        self.addWidget(self.ftpLoginView)
        self.addWidget(self.directoryView)
        self.addWidget(self.fileView)
        self.addWidget(self.toolsView)


        ## Set window title, set geometry and show
        self.setWindowTitle('ScriptBook')
        self.setGeometry(400, 200, 280, 430)
        self.show()

        ## Load settings
        self.loadSettings()

        ## Load documents
        self.loadDocuments()


    def toolsClicked(self, entry):
        print 'toolsClicked ', entry
        if int(entry) == 0:
            self.setCurrentWidget(self.ftpLoginView)


    def ftpConnect(self, host, port):
        self.ftpEntryListController.setHostPort(host, port)
        self.ftpEntryListController.setDirectory(".")
        self.ftpDirectoryListRequest()

    def ftpCancel(self):
        print 'ftpCancel'
        self.setCurrentWidget(self.toolsView)


    def ftpDirectoryListRequest(self):
        print 'ftpDirectoryListRequest'
        self.ftpEntryListController.directoryList()


    def ftpDirectoryListDone(self):
        print 'ftpDirectoryListDone'
        directoryListItems = []
        directories = self.ftpEntryListController.list()
        #print 'directories', directories
        if len(directories) > int(0):
            for d in directories:
                directoryListItems.append(DirectoryList.DirectoryListWrapper(str(d)))
                print d

            self.directoryList = DirectoryList.DirectoryModel(directoryListItems)
            self.directoryView.rootContext().setContextProperty('directoryListModel', self.directoryList)
            self.setCurrentWidget(self.directoryView)


    def directoryClicked(self, name):
        print 'directoryClicked', name
        self.ftpEntryListController.setDirectory(name)
        self.ftpEntryListController.fileList()


    def ftpFileListDone(self):
        print 'ftpFileListDone'
        fileListItems = []
        files = self.ftpEntryListController.list()
        if len(files) > int(0):
            print 'Directory contains', len(files), "entries"
            for f in files:
                fileListItems.append(FileList.FileListWrapper(str(f)))
                print f

            self.fileList = FileList.FileModel(fileListItems)
            self.fileView.rootContext().setContextProperty('fileListModel', self.fileList)
            self.setCurrentWidget(self.fileView)



    def fileClicked(self, name):
        print 'fileClicked'


    def loadDocuments(self):
        documentListItems = []        
        dirFilter = []
        dirFilter.append('*.xml')
        directory = QtCore.QDir()
        dirList = directory.entryList(dirFilter)
        if len(dirList) > 0:
            count = int(1)
            for entry in directory.entryInfoList(dirFilter):
                documentListItems.append(DocumentList.DocumentListWrapper(str(count), str(entry.size()), str(entry.fileName())))
                count += 1

        self.documentList = DocumentList.DocumentModel(documentListItems)
        self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)



    def loadSettings(self):
        ## Read the settings
        settings = QtCore.QSettings()

        ## The ftp host and port
        self.ftpHost = settings.value("ScriptBook/ftpHost", "localhost")
        self.ftpPort = settings.value("ScriptBook/ftpPort", "21")

        ## Update the view through the controller
        self.ftpController.setHost(self.ftpHost)
        self.ftpController.onHostChanged.emit(str(self.ftpHost))
        self.ftpController.setPort(self.ftpPort)
        self.ftpController.onPortChanged.emit(str(self.ftpPort))


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
            self.setCurrentWidget(self.verseView)
        elif button == 4:
            self.setCurrentWidget(self.toolsView)


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
