# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide import QtGui
from PySide import QtXml

import Document

class DocumentXmlHandler(QtXml.QXmlDefaultHandler):
    def __init__(self):
        super(DocumentXmlHandler, self).__init__()

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
            self.errorStr = str("Start Element: Not a script book file")
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

        else:
            self.errorStr = str("Start Element: unknown qName")

        return True


    def endElement(self, namespaceURI, localName, qName):
        if qName == 'document':
            self.errorStr = str("End element qName not a script book")
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

        else:
            self.errorStr = str("End element: Unknown qName")

        return True


    def fatalError(self, exception):
        return False

    def errorString(self):
        return self.errorStr

    def createChildItem(self, tagName):
        return childItem
