#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtXml
from PySide import QtDeclarative


## Import the python directory and import files from it
sys.path.append('python')


## The XML handler
import DocumentXmlHandler

## Document class defenition
from Document import *

## The controllers
from ToolsController import *
from FtpController import *
from FtpEntryListController import *

## The list view's Model, Wrapper and Controller
from BookList import *
from ChapterList import *
from VerseList import *
from DocumentList import *
from DirectoryList import *
import FileList


## The Controller for the navigation buttons
class NavigationController(QtCore.QObject):
    buttonClicked = QtCore.Signal(int)

    _button = int(-1)

    def __init__(self, parent = None):
        super(NavigationController, self).__init__(parent)
        self.buttonClicked.connect(self.clicked)


    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def clicked(self, button):
        #global view, __doc__ #### view ???
        self._button = button
        print 'NavigationController::CLICKED', button, self._button


    @QtCore.Slot(QtCore.QObject)
    def _gradient(self):
        print 'NavigationController::_GRADIENT', self._button
        return int(self._button)

    gradient = QtCore.Property(int, _gradient, notify=buttonClicked)


class WidgetIndex:
    DocumentView = 0
    BookView = 1
    ChapterView = 2
    VerseView = 3
    FtpLoginView = 4
    DirectoryView = 5
    FileView = 6
    ToolsView = 7
    DownloadingView = 8
    DownloadDoneView = 9
    LoadingDocumentView = 10


class ScriptBook(QtGui.QStackedWidget):
    ## The set widget index signal
    setWidgetIndexSignal = QtCore.Signal(int)

    ## The set previous index signal
    setPreviousIndexSignal = QtCore.Signal()

    ## current index
    _widget_index = int(-1)

    ## previous index
    _previous_index = int(-1)

    ## set index slot
    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def set_widget_index(self, index):
        print 'DEBUG set_widget_index', index

        self._previous_index = self._widget_index
        self.setCurrentIndex(index)
        self._widget_index = index

    ## set previous index slot
    @QtCore.Slot(QtCore.QObject)
    def set_previous_index(self):
        print 'DEBUG set_previous_index'

        self.setCurrentIndex(self._previous_index)
        previous = self._previous_index
        self._previous_index = self._widget_index
        self._widget_index = previous



    def __init__(self, parent=None):
        super(ScriptBook, self).__init__(parent)

        self.setWidgetIndexSignal.connect(self.set_widget_index)
        self.setPreviousIndexSignal.connect(self.set_previous_index)

        self.document = Document()
        self.handler = DocumentXmlHandler.DocumentXmlHandler()

        ## Set values for the store/restore settings system
        QtCore.QCoreApplication.setOrganizationName("EMR")
        QtCore.QCoreApplication.setOrganizationDomain("code.rutger.no")
        QtCore.QCoreApplication.setApplicationName("ScriptBook")

        ## The button controller
        self.buttonController = NavigationController()
        self.buttonController.buttonClicked.connect(self.buttonClicked)

        ## The tools controller
        self.toolsController = ToolsController()
        self.toolsController.toolsClicked.connect(self.toolsClicked)

        ## The ftp login controller
        self.ftpController = FtpController()
        self.ftpController.connectSignal.connect(self.ftpConnect)
        self.ftpController.cancelSignal.connect(self.ftpCancel)

        ## The ftp entry list controller
        self.ftpEntryListController = FtpEntryListController()
        self.ftpEntryListController.ftpDirectoryListDone.connect(self.ftpDirectoryListDone)
        self.ftpEntryListController.ftpFileListDone.connect(self.ftpFileListDone)
        self.ftpEntryListController.ftpDownloadDone.connect(self.ftpDownloadDone)
        self.ftpEntryListController.ftpDownloading.connect(self.ftpDownloading)
        self.ftpEntryListController.ftpReadyRead.connect(self.ftpReadyRead)


        ## Set up UI components
        self.setupUI()


    def setupUI(self):
        ## The document view, controller and  model
        self.documentView = QtDeclarative.QDeclarativeView()
        self.documentView.setWindowTitle('Documents')
        self.documentView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.documentController = DocumentController()
        self.documentController.documentClicked.connect(self.documentClicked)
        self.documentView.rootContext().setContextProperty('controller', self.documentController)
        self.documentView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.documentList = DocumentModel([])
        self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)
        self.documentView.setSource(QtCore.QUrl('qml/DocumentListModel.qml'))


        ## The book view, controller and  model
        self.bookView = QtDeclarative.QDeclarativeView()
        self.bookView.setWindowTitle('Books')
        self.bookView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.bookController = BookController()
        self.bookController.bookClicked.connect(self.bookClicked)
        self.bookView.rootContext().setContextProperty('controller', self.bookController)
        self.bookView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.bookList = BookModel([])
        self.bookView.rootContext().setContextProperty('bookListModel', self.bookList)
        self.bookView.setSource(QtCore.QUrl('qml/BookListModel.qml'))

        ## The chapter view, controller and  model
        self.chapterView = QtDeclarative.QDeclarativeView()
        self.chapterView.setWindowTitle('Chapter')
        self.chapterView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.chapterController = ChapterController()
        self.chapterController.chapterClicked.connect(self.chapterClicked)
        self.chapterView.rootContext().setContextProperty('controller', self.chapterController)
        self.chapterView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.chapterList = ChapterModel([])
        self.chapterView.rootContext().setContextProperty('chapterListModel', self.chapterList)
        self.chapterView.setSource(QtCore.QUrl('qml/ChapterListModel.qml'))

        ## The chapter view, controller and  model
        self.verseView = QtDeclarative.QDeclarativeView()
        self.verseView.setWindowTitle('Verse')
        self.verseView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.verseController = VerseController()
        self.verseController.verseClicked.connect(self.verseClicked)
        self.verseView.rootContext().setContextProperty('controller', self.verseController)
        self.verseView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.verseList = VerseModel([])
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
        self.directoryController = DirectoryController()
        self.directoryController.directoryClicked.connect(self.directoryClicked)
        self.directoryView.rootContext().setContextProperty('controller', self.directoryController)
        self.directoryList = DirectoryModel([])
        self.directoryView.rootContext().setContextProperty('directoryListModel', self.directoryList)
        self.directoryView.rootContext().setContextProperty('ftpController', self.ftpController)
        self.directoryView.setSource(QtCore.QUrl('qml/FtpDirectoryListModel.qml'))
        self.directoryView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The ftp file view
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
        self.fileView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The downloading view
        self.downloadingView = QtDeclarative.QDeclarativeView()
        self.downloadingView.setWindowTitle('Download Done')
        self.downloadingView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.downloadingView.setSource(QtCore.QUrl('qml/Downloading.qml'))
        self.downloadingView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The download done view
        self.downloadDoneView = QtDeclarative.QDeclarativeView()
        self.downloadDoneView.setWindowTitle('Download Done')
        self.downloadDoneView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.downloadDoneView.setSource(QtCore.QUrl('qml/DownloadDone.qml'))
        self.downloadDoneView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The loading document view
        self.loadingDocumentView = QtDeclarative.QDeclarativeView()
        self.loadingDocumentView.setWindowTitle('Loading Document')
        self.loadingDocumentView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.loadingDocumentView.setSource(QtCore.QUrl('qml/LoadingDocument.qml'))
        self.loadingDocumentView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## Add the book, chapter and verse view's
        self.addWidget(self.documentView)
        self.addWidget(self.bookView)
        self.addWidget(self.chapterView)
        self.addWidget(self.verseView)
        self.addWidget(self.ftpLoginView)
        self.addWidget(self.directoryView)
        self.addWidget(self.fileView)
        self.addWidget(self.toolsView)
        self.addWidget(self.downloadingView)
        self.addWidget(self.downloadDoneView)
        self.addWidget(self.loadingDocumentView)

        ## Set window title, set geometry and show
        self.setWindowTitle('ScriptBook')
        self.setGeometry(400, 200, 280, 430)
        self.show()

        ## Load settings
        self.loadSettings()

        ## Load documents
        self.displayDocuments()

        print 'DEBUG emiting set widget index signal'
        self.setWidgetIndexSignal.emit(WidgetIndex().LoadingDocumentView)


    def ftpReadyRead(self, bytes):
        print 'readyRead bytes:', bytes


    ## Reackt on Tool Button Click
    def toolsClicked(self, entry):
        if int(entry) == 0:
            self.setWidgetIndexSignal.emit(WidgetIndex().FtpLoginView)
            #self.setCurrentWidget(self.ftpLoginView)
        elif int(entry) == 1:
            print 'toolsClicked: Font settings - not implemented'
        elif int(entry) == 2:
            print 'toolsClicked: Bookmars - not implemented'
        else:
            print 'toolsClicked: unknonw'


    def ftpConnect(self, host, port):
        self.ftpEntryListController.setHostPort(host, port)
        self.ftpEntryListController.setDirectory(".")
        self.ftpEntryListController.directoryList()


    def ftpCancel(self):
        if self.currentWidget() == self.fileView:
            self.setWidgetIndexSignal.emit(WidgetIndex().DirectoryView)
            #self.setCurrentWidget(self.directoryView)
        elif self.currentWidget() == self.directoryView:
            self.setWidgetIndexSignal.emit(WidgetIndex().FtpLoginView)
            #self.setCurrentWidget(self.ftpLoginView)
        elif self.currentWidget() == self.ftpLoginView:
            self.setWidgetIndexSignal.emit(WidgetIndex().ToolsView)
            #self.setCurrentWidget(self.toolsView)
        else:
            self.setWidgetIndexSignal.emit(WidgetIndex().ToolsView)
            #self.setCurrentWidget(self.toolsView)


    def ftpDirectoryListDone(self):
        print 'ftpDirectoryListDone'
        directoryListItems = []
        directories = self.ftpEntryListController.list()
        #print 'directories', directories
        if len(directories) > int(0):
            for d in directories:
                directoryListItems.append(DirectoryListWrapper(str(d)))
                print d

            self.directoryList = DirectoryModel(directoryListItems)
            self.directoryView.rootContext().setContextProperty('directoryListModel', self.directoryList)
            self.setWidgetIndexSignal.emit(WidgetIndex().DirectoryView)
            #self.setCurrentWidget(self.directoryView)


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
            self.setWidgetIndexSignal.emit(WidgetIndex().FileView)
            #self.setCurrentWidget(self.fileView)


    def ftpDownloading(self):
        print 'ftpDownloading'
        self.setWidgetIndexSignal.emit(WidgetIndex().DownloadingView)
        #self.setCurrentWidget(self.downloadingView)


    def ftpDownloadDone(self):
        ## Get content to local variable
        self._downloadedFile = self.ftpEntryListController.getFile()

        print 'ftpDownloadDone', len(self._downloadedFile)

        ## Write content to file
        f = open(self._filename, "w")
        f.write(self._downloadedFile)
        f.close()

        ## Set Download done Widget
        self.setWidgetIndexSignal.emit(WidgetIndex().DownloadDoneView)


    def fileClicked(self, name):
        print 'fileClicked', name
        if name != str(""):
            self._filename = name
            self.ftpEntryListController.downloadFile(self._filename)


    def findXmlFiles(self):
        xmlFiles = []
        directory = QtCore.QDir()

        ## Go through directory content and look for xml files
        for e in directory.entryList():
            if e == '.' or e == '..':
                continue

            ## Split filename string on '.' and check if last part is 'xml'
            f = e.split('.')
            if len(f) == 2:
                if f[1] == 'xml':
                    ## XML file - append
                    xmlFiles.append(e)

        return xmlFiles


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

        ## Look for xml files in directory
        xmlFiles = self.findXmlFiles()

        ## If we don't have any xml files, load ftp login view
        if len(xmlFiles) == 0:
            self.setWidgetIndexSignal.emit(WidgetIndex().FtpLoginView)
            #self.setCurrentWidget(self.ftpLoginView)
            return

        ## If there are no document give we cannot preload anything
        if document == None:
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
            return

        ## If we don't have the requested document we cannot preload it
        if xmlFiles.__contains__(str(document)) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
            return

        ## If we fail to open the file, set document view as page
        if self.openFile(document) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
            return

        ## If book is not give, load the book view
        if book == None:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)
            return

        ## SHOULD GIVE PROPER ERROR PAGE HERE
        if self.loadBook(int(book)) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)
            return

        ## If chapter is not give, show chapter view
        if chapter == None:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
            return

        ## SHOULD GIVE PROPER ERROR PAGE HERE
        if self.loadChapter(int(chapter)) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
            return

        self.setWidgetIndexSignal.emit(WidgetIndex().VerseView)
        #self.setCurrentWidget(self.verseView)
            

    def displayDocuments(self):
        documentListItems = []        
        dirFilter = []
        dirFilter.append('*.xml')
        directory = QtCore.QDir()
        dirList = directory.entryList(dirFilter)
        if len(dirList) > 0:
            count = int(1)
            for entry in directory.entryInfoList(dirFilter):
                documentListItems.append(DocumentListWrapper(str(count), str(entry.size()), str(entry.fileName())))
                count += 1

            self.documentList = DocumentModel(documentListItems)
            self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)

        else:
            print 'No XML files in directory' # TBD Inform user


    def documentClicked(self, document):
        #print 'documentClicked', document

        if self.openFile(document) == True:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)


    def loadBook(self, book):
        chapterListItems = []

        try: ## TBD inform user - rewrite this
            books = self.document.books()
            for b in books:
                if int(b.document_entry) == int(book):
                    ## Book requested found
                    self.book = b

                    ## Append chapters in book into chapterListItems
                    chapters = self.book.chap()
                    for c in chapters:
                        chapterListItems.append(ChapterListWrapper(c.no, c.verses, c.vers()[0].text))
                    break

            self.chapterList = ChapterModel(chapterListItems)
            self.chapterView.rootContext().setContextProperty('chapterListModel', self.chapterList)
            return True
        except:
            return False


    def bookClicked(self, book):
        if self.loadBook(book) == True:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
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
                        verseListItems.append(VerseListWrapper(int(i.number), textstring))
                        #verseListItems.append(VerseListWrapper(int(i.number), str(i.text)))
                    break

            self.verseList = VerseModel(verseListItems)
            self.verseView.rootContext().setContextProperty('verseListModel', self.verseList)
            return True
        except:
            print 'loadChapter failed'
            return False


    def chapterClicked(self, chapter):
        if self.loadChapter(chapter) == True:
            self.setWidgetIndexSignal.emit(WidgetIndex().VerseView)
            #self.setCurrentWidget(self.verseView)

            ## Write bookmark to settings
            settings = QtCore.QSettings()
            settings.setValue("ScriptBook/verse", "1")                       ## Reset verse to first vers
            settings.setValue("ScriptBook/chapter", chapter)                 ## Write chapter
            settings.setValue("ScriptBook/book", self.book.document_entry)   ## Book is not stored before a chapter is choosen


    def verseClicked(self, verse):
        ## Write the verse to settings (needed ?)
        ## Note what verse was clicked (we wind to this place at restore) - do this more dynamic (onContenYChanged ?)
        settings = QtCore.QSettings()
        settings.setValue("ScriptBook/verse", verse)

        ## Shoud give pop up options here
        ## 1. Save bookmark
        ## 2. Save note
        ## 3. Higlight (set different font and background color)


    def buttonClicked(self, button):
        print 'buttonClicked: button', button
        if button == 0:
            self.displayDocuments()
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
        elif button == 1:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)
        elif button == 2:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
        elif button == 3:
            self.setWidgetIndexSignal.emit(WidgetIndex().VerseView)
            #self.setCurrentWidget(self.verseView)
        elif button == 4:
            self.setWidgetIndexSignal.emit(WidgetIndex().ToolsView)
            #self.setCurrentWidget(self.toolsView)

        ## Back button on Donwload done
        elif button == 10:
            print 'button == 10'
            self.setWidgetIndexSignal.emit(WidgetIndex().FileView)
            #self.setCurrentWidget(self.fileView)

        ## Cancel download
        elif button == 11:
            print 'button == 11 Cancel button'
            self.setPreviousIndexSignal.emit()

        elif button == 12:
            print'button == 12 Load document (self._filename)'
            if self.openFile(self._filename) == True:
                self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
                #self.setCurrentWidget(self.bookView)


    def loadDocument(self):
        self.bookListItems = []

        books = self.document.books()
        for b in books:
            self.bookListItems.append(BookListWrapper(b.document_entry, b.name, b.chapters))

        return True


    def openFile(self, filename):

        ## Open xml file
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "ScriptBook", "Cannot read file \n%s:\n." % filename)
            self.setPreviousIndexSignal.emit()
            return False

        ## Initialize xml reader
        reader = QtXml.QXmlSimpleReader()

        ## Set values for the store/restore settings system
        QtCore.QCoreApplication.setOrganizationName("EMR")
        QtCore.QCoreApplication.setOrganizationDomain("code.rutger.no")
        QtCore.QCoreApplication.setApplicationName("ScriptBook")

        ## The button controller
        self.buttonController = NavigationController()
        self.buttonController.buttonClicked.connect(self.buttonClicked)

        ## The tools controller
        self.toolsController = ToolsController()
        self.toolsController.toolsClicked.connect(self.toolsClicked)

        ## The ftp login controller
        self.ftpController = FtpController()
        self.ftpController.connectSignal.connect(self.ftpConnect)
        self.ftpController.cancelSignal.connect(self.ftpCancel)

        ## The ftp entry list controller
        self.ftpEntryListController = FtpEntryListController()
        self.ftpEntryListController.ftpDirectoryListDone.connect(self.ftpDirectoryListDone)
        self.ftpEntryListController.ftpFileListDone.connect(self.ftpFileListDone)
        self.ftpEntryListController.ftpDownloadDone.connect(self.ftpDownloadDone)
        self.ftpEntryListController.ftpDownloading.connect(self.ftpDownloading)
        self.ftpEntryListController.ftpReadyRead.connect(self.ftpReadyRead)


        ## Set up UI components
        self.setupUI()


    def setupUI(self):
        ## The document view, controller and  model
        self.documentView = QtDeclarative.QDeclarativeView()
        self.documentView.setWindowTitle('Documents')
        self.documentView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.documentController = DocumentController()
        self.documentController.documentClicked.connect(self.documentClicked)
        self.documentView.rootContext().setContextProperty('controller', self.documentController)
        self.documentView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.documentList = DocumentModel([])
        self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)
        self.documentView.setSource(QtCore.QUrl('qml/DocumentListModel.qml'))


        ## The book view, controller and  model
        self.bookView = QtDeclarative.QDeclarativeView()
        self.bookView.setWindowTitle('Books')
        self.bookView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.bookController = BookController()
        self.bookController.bookClicked.connect(self.bookClicked)
        self.bookView.rootContext().setContextProperty('controller', self.bookController)
        self.bookView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.bookList = BookModel([])
        self.bookView.rootContext().setContextProperty('bookListModel', self.bookList)
        self.bookView.setSource(QtCore.QUrl('qml/BookListModel.qml'))

        ## The chapter view, controller and  model
        self.chapterView = QtDeclarative.QDeclarativeView()
        self.chapterView.setWindowTitle('Chapter')
        self.chapterView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.chapterController = ChapterController()
        self.chapterController.chapterClicked.connect(self.chapterClicked)
        self.chapterView.rootContext().setContextProperty('controller', self.chapterController)
        self.chapterView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.chapterList = ChapterModel([])
        self.chapterView.rootContext().setContextProperty('chapterListModel', self.chapterList)
        self.chapterView.setSource(QtCore.QUrl('qml/ChapterListModel.qml'))

        ## The chapter view, controller and  model
        self.verseView = QtDeclarative.QDeclarativeView()
        self.verseView.setWindowTitle('Verse')
        self.verseView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.verseController = VerseController()
        self.verseController.verseClicked.connect(self.verseClicked)
        self.verseView.rootContext().setContextProperty('controller', self.verseController)
        self.verseView.rootContext().setContextProperty('buttonController', self.buttonController)
        self.verseList = VerseModel([])
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
        self.directoryController = DirectoryController()
        self.directoryController.directoryClicked.connect(self.directoryClicked)
        self.directoryView.rootContext().setContextProperty('controller', self.directoryController)
        self.directoryList = DirectoryModel([])
        self.directoryView.rootContext().setContextProperty('directoryListModel', self.directoryList)
        self.directoryView.rootContext().setContextProperty('ftpController', self.ftpController)
        self.directoryView.setSource(QtCore.QUrl('qml/FtpDirectoryListModel.qml'))
        self.directoryView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The ftp file view
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
        self.fileView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The downloading view
        self.downloadingView = QtDeclarative.QDeclarativeView()
        self.downloadingView.setWindowTitle('Download Done')
        self.downloadingView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.downloadingView.setSource(QtCore.QUrl('qml/Downloading.qml'))
        self.downloadingView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The download done view
        self.downloadDoneView = QtDeclarative.QDeclarativeView()
        self.downloadDoneView.setWindowTitle('Download Done')
        self.downloadDoneView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.downloadDoneView.setSource(QtCore.QUrl('qml/DownloadDone.qml'))
        self.downloadDoneView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## The loading document view
        self.loadingDocumentView = QtDeclarative.QDeclarativeView()
        self.loadingDocumentView.setWindowTitle('Loading Document')
        self.loadingDocumentView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.loadingDocumentView.setSource(QtCore.QUrl('qml/LoadingDocument.qml'))
        self.loadingDocumentView.rootContext().setContextProperty('buttonController', self.buttonController)

        ## Add the book, chapter and verse view's
        self.addWidget(self.documentView)
        self.addWidget(self.bookView)
        self.addWidget(self.chapterView)
        self.addWidget(self.verseView)
        self.addWidget(self.ftpLoginView)
        self.addWidget(self.directoryView)
        self.addWidget(self.fileView)
        self.addWidget(self.toolsView)
        self.addWidget(self.downloadingView)
        self.addWidget(self.downloadDoneView)
        self.addWidget(self.loadingDocumentView)

        ## Set window title, set geometry and show
        self.setWindowTitle('ScriptBook')
        self.setGeometry(400, 200, 280, 430)
        self.show()

        ## Load settings
        self.loadSettings()

        ## Load documents
        self.displayDocuments()

        print 'DEBUG emiting set widget index signal'
        #self.setWidgetIndexSignal.emit(WidgetIndex().LoadingDocumentView)


    def ftpReadyRead(self, bytes):
        print 'readyRead bytes:', bytes


    ## Reackt on Tool Button Click
    def toolsClicked(self, entry):
        if int(entry) == 0:
            self.setWidgetIndexSignal.emit(WidgetIndex().FtpLoginView)
            #self.setCurrentWidget(self.ftpLoginView)
        elif int(entry) == 1:
            print 'toolsClicked: Font settings - not implemented'
        elif int(entry) == 2:
            print 'toolsClicked: Bookmars - not implemented'
        else:
            print 'toolsClicked: unknonw'


    def ftpConnect(self, host, port):
        self.ftpEntryListController.setHostPort(host, port)
        self.ftpEntryListController.setDirectory(".")
        self.ftpEntryListController.directoryList()


    def ftpCancel(self):
        if self.currentWidget() == self.fileView:
            self.setWidgetIndexSignal.emit(WidgetIndex().DirectoryView)
            #self.setCurrentWidget(self.directoryView)
        elif self.currentWidget() == self.directoryView:
            self.setWidgetIndexSignal.emit(WidgetIndex().FtpLoginView)
            #self.setCurrentWidget(self.ftpLoginView)
        elif self.currentWidget() == self.ftpLoginView:
            self.setWidgetIndexSignal.emit(WidgetIndex().ToolsView)
            #self.setCurrentWidget(self.toolsView)
        else:
            self.setWidgetIndexSignal.emit(WidgetIndex().ToolsView)
            #self.setCurrentWidget(self.toolsView)


    def ftpDirectoryListDone(self):
        print 'ftpDirectoryListDone'
        directoryListItems = []
        directories = self.ftpEntryListController.list()
        #print 'directories', directories
        if len(directories) > int(0):
            for d in directories:
                directoryListItems.append(DirectoryListWrapper(str(d)))
                print d

            self.directoryList = DirectoryModel(directoryListItems)
            self.directoryView.rootContext().setContextProperty('directoryListModel', self.directoryList)
            self.setWidgetIndexSignal.emit(WidgetIndex().DirectoryView)
            #self.setCurrentWidget(self.directoryView)


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
            self.setWidgetIndexSignal.emit(WidgetIndex().FileView)
            #self.setCurrentWidget(self.fileView)


    def ftpDownloading(self):
        print 'ftpDownloading'
        self.setWidgetIndexSignal.emit(WidgetIndex().DownloadingView)
        #self.setCurrentWidget(self.downloadingView)


    def ftpDownloadDone(self):
        ## Get content to local variable
        self._downloadedFile = self.ftpEntryListController.getFile()

        print 'ftpDownloadDone', len(self._downloadedFile)

        ## Write content to file
        f = open(self._filename, "w")
        f.write(self._downloadedFile)
        f.close()

        ## Set Download done Widget
        self.setWidgetIndexSignal.emit(WidgetIndex().DownloadDoneView)


    def fileClicked(self, name):
        print 'fileClicked', name
        if name != str(""):
            self._filename = name
            self.ftpEntryListController.downloadFile(self._filename)


    def findXmlFiles(self):
        xmlFiles = []
        directory = QtCore.QDir()

        ## Go through directory content and look for xml files
        for e in directory.entryList():
            if e == '.' or e == '..':
                continue

            ## Split filename string on '.' and check if last part is 'xml'
            f = e.split('.')
            if len(f) == 2:
                if f[1] == 'xml':
                    ## XML file - append
                    xmlFiles.append(e)

        return xmlFiles


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

        ## Look for xml files in directory
        xmlFiles = self.findXmlFiles()

        ## If we don't have any xml files, load ftp login view
        if len(xmlFiles) == 0:
            self.setWidgetIndexSignal.emit(WidgetIndex().FtpLoginView)
            #self.setCurrentWidget(self.ftpLoginView)
            return

        ## If there are no document give we cannot preload anything
        if document == None:
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
            return

        ## If we don't have the requested document we cannot preload it
        if xmlFiles.__contains__(str(document)) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
            return

        ## If we fail to open the file, set document view as page
        if self.openFile(document) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
            return

        ## If book is not give, load the book view
        if book == None:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)
            return

        ## SHOULD GIVE PROPER ERROR PAGE HERE
        if self.loadBook(int(book)) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)
            return

        ## If chapter is not give, show chapter view
        if chapter == None:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
            return

        ## SHOULD GIVE PROPER ERROR PAGE HERE
        if self.loadChapter(int(chapter)) == False:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
            return

        self.setWidgetIndexSignal.emit(WidgetIndex().VerseView)
        #self.setCurrentWidget(self.verseView)
            

    def displayDocuments(self):
        documentListItems = []        
        dirFilter = []
        dirFilter.append('*.xml')
        directory = QtCore.QDir()
        dirList = directory.entryList(dirFilter)
        if len(dirList) > 0:
            count = int(1)
            for entry in directory.entryInfoList(dirFilter):
                documentListItems.append(DocumentListWrapper(str(count), str(entry.size()), str(entry.fileName())))
                count += 1

            self.documentList = DocumentModel(documentListItems)
            self.documentView.rootContext().setContextProperty('documentListModel', self.documentList)

        else:
            print 'No XML files in directory' # TBD Inform user


    def documentClicked(self, document):
        #print 'documentClicked', document

        if self.openFile(document) == True:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)


    def loadBook(self, book):
        chapterListItems = []

        try: ## TBD inform user - rewrite this
            books = self.document.books()
            for b in books:
                if int(b.document_entry) == int(book):
                    ## Book requested found
                    self.book = b

                    ## Append chapters in book into chapterListItems
                    chapters = self.book.chap()
                    for c in chapters:
                        chapterListItems.append(ChapterListWrapper(c.no, c.verses, c.vers()[0].text))
                    break

            self.chapterList = ChapterModel(chapterListItems)
            self.chapterView.rootContext().setContextProperty('chapterListModel', self.chapterList)
            return True
        except:
            return False


    def bookClicked(self, book):
        if self.loadBook(book) == True:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
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
                        verseListItems.append(VerseListWrapper(int(i.number), textstring))
                        #verseListItems.append(VerseListWrapper(int(i.number), str(i.text)))
                    break

            self.verseList = VerseModel(verseListItems)
            self.verseView.rootContext().setContextProperty('verseListModel', self.verseList)
            return True
        except:
            print 'loadChapter failed'
            return False


    def chapterClicked(self, chapter):
        if self.loadChapter(chapter) == True:
            self.setWidgetIndexSignal.emit(WidgetIndex().VerseView)
            #self.setCurrentWidget(self.verseView)

            ## Write bookmark to settings
            settings = QtCore.QSettings()
            settings.setValue("ScriptBook/verse", "1")                       ## Reset verse to first vers
            settings.setValue("ScriptBook/chapter", chapter)                 ## Write chapter
            settings.setValue("ScriptBook/book", self.book.document_entry)   ## Book is not stored before a chapter is choosen


    def verseClicked(self, verse):
        ## Write the verse to settings (needed ?)
        ## Note what verse was clicked (we wind to this place at restore) - do this more dynamic (onContenYChanged ?)
        settings = QtCore.QSettings()
        settings.setValue("ScriptBook/verse", verse)

        ## Shoud give pop up options here
        ## 1. Save bookmark
        ## 2. Save note
        ## 3. Higlight (set different font and background color)


    def buttonClicked(self, button):
        print 'buttonClicked: button', button
        if button == 0:
            self.displayDocuments()
            self.setWidgetIndexSignal.emit(WidgetIndex().DocumentView)
            #self.setCurrentWidget(self.documentView)
        elif button == 1:
            self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
            #self.setCurrentWidget(self.bookView)
        elif button == 2:
            self.setWidgetIndexSignal.emit(WidgetIndex().ChapterView)
            #self.setCurrentWidget(self.chapterView)
        elif button == 3:
            self.setWidgetIndexSignal.emit(WidgetIndex().VerseView)
            #self.setCurrentWidget(self.verseView)
        elif button == 4:
            self.setWidgetIndexSignal.emit(WidgetIndex().ToolsView)
            #self.setCurrentWidget(self.toolsView)

        ## Back button on Donwload done
        elif button == 10:
            print 'button == 10'
            self.setWidgetIndexSignal.emit(WidgetIndex().FileView)
            #self.setCurrentWidget(self.fileView)

        ## Cancel download
        elif button == 11:
            print 'button == 11 Cancel button'
            self.setPreviousIndexSignal.emit()

        elif button == 12:
            print'button == 12 Load document (self._filename)'
            if self.openFile(self._filename) == True:
                self.setWidgetIndexSignal.emit(WidgetIndex().BookView)
                #self.setCurrentWidget(self.bookView)


    def loadDocument(self):
        self.bookListItems = []

        books = self.document.books()
        for b in books:
            self.bookListItems.append(BookListWrapper(b.document_entry, b.name, b.chapters))

        return True


    def openFile(self, filename):

        ## Open xml file
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "ScriptBook", "Cannot read file \n%s:\n." % filename)
            self.setPreviousIndexSignal.emit()
            return False

        ## Initialize xml reader
        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(self.handler)
        reader.setErrorHandler(self.handler)

        ## xml input source
        xmlInputSource = QtXml.QXmlInputSource(file)

        ## Set loading document widget
        self.setWidgetIndexSignal.emit(WidgetIndex().LoadingDocumentView)

        ## Parse xml file
        if reader.parse(xmlInputSource) == False:
            print "openFile Error:", self.handler.errorString()
            QtGui.QMessageBox.warning(self, "ScriptBook", "Cannot parse file \n%s\n  %s\n" % (filename, self.handler.errorString()))
            self.setPreviousIndexSignal.emit()
            return False

        ## Copy document from the xml handler
        self.document = self.handler.document

        ## Check document
        if self.document.checkDocument() == False:
            print 'Loading documet failed'
            self.setPreviousIndexSignal.emit()
            return False

        ## Load Document
        if (self.loadDocument() == False):
            print 'openFile: loadDocument failed'
            self.setPreviousIndexSignal.emit()
            return False

        ## Populate book list
        self.bookList = BookModel(self.bookListItems)
        self.bookView.rootContext().setContextProperty('bookListModel', self.bookList)

        ## Set window title
        self.setWindowTitle(str(("ScriptBook %s" % self.document.description)))

        ## Backup settings
        settings = QtCore.QSettings()
        settings.setValue("ScriptBook/document", filename)
        settings.setValue("ScriptBook/book", None)
        settings.setValue("ScriptBook/chapter", None)
        settings.setValue("ScriptBook/verse", None)

        ## Set the previous widget (current is LoadinDocumentView), the caller should set the apropriate widget
        self.setPreviousIndexSignal.emit()

        return True


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    scriptBook = ScriptBook()
    sys.exit(app.exec_())
