# -*- coding: utf-8 -*-

class Vers():
    number = int(0)
    text = str("")

    def __init__(self):
        self.number = int(0)
        self.text = str("")

    def printVers(self):
        print "v", self.number, " ", self.text


class Chapter():
    __verses = []
    __comments = []

    no = int(0)
    verses = int(0)

    def __init__(self):
        self.__verses = []
        self.__comments = []
        self.no = int(0)
        self.verses = int(0)

    def vers(self):
        return self.__verses

    def appendVers(self, vers):
        if vers.number != 0:
            self.__verses.append(vers)

    def printVerses(self):
        print 'Chapter', self.no
        for i in self.__verses:
            i.printVers()


class Book():
    __chapters = []

    name = str("")
    document_entry = int(0)
    chapters = int(0)

    def __init__(self):
        self.__chapters = []
        self.name = str("")
        self.document_entry = int(0)
        self.chapters = int(0)

    def append(self, chapter):
        if chapter.verses != 0:
            self.__chapters.append(chapter)

    def chap(self):
        return self.__chapters
    
    def printBook(self):
        print 'Book', self.name
        for i in self.__chapters:
            i.printVerses()


class Document():
    __books = []

    description = str("")
    language = str("")
    entries = int(0)

    def __init__(self):
        self.__books = []
        self.description = str("")
        self.language = str("")
        self.entries = int(0)

    def append(self, book):
        if book.chapters != 0:
            self.__books.append(book)

    def books(self):
        return self.__books

    def printDocument(self):
        print 'Document', self.description
        for i in self.__books:
            i.printBook()

