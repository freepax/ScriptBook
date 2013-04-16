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

    def checkChapter(self):
        ## Check that the chapter contains the number of verses as it clames
        if len(self.__verses) != int(self.verses):
            print 'Chapter::checkChapter Verses entries check failed'
            return False

        ## Check all the verses
        count = int(1)
        for vers in self.__verses:
            ## Check that the vers number increases from vers to the next
            if int(vers.number) != count:
                print 'Chapter::checkChapter: verse number check failed (verse', count, ')', vers.number
                return False

            ## Increase the verse counter
            count = int(count + 1)


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

    def checkBook(self):
        print 'Book::checkBook len:', len(self.__chapters), "chapters", self.chapters
        if len(self.__chapters) != int(self.chapters):
            print 'Book::checkBook: Chapters error'
            return False

        count = int(1)
        for chapter in self.__chapters:
            ## Check that the chapter number is incrementing correctly from chapter to the next
            if int(chapter.no) != int(count):
                print 'Book::checkBook: Chapter number error (', count, ')', chapter.no
                return False

            ## Check this chapter
            elif chapter.checkChapter() == False:
                print 'Book::checkBook: checkChapter failed(', count, ')'
                return False

            ## Increment the chapter counter
            count = int(count + 1)


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

    def checkDocument(self):
        ## Check that the book contains as many books as it clames
        if len(self.__books) != int(self.entries):
            print 'Document::checkDocument Books and Entries missmatch in document'
            return False

        ## Go through all books
        count = int(1)
        for book in self.__books:
            
            ## Check that the document entry increases correctly from entry to the next
            if int(book.document_entry) != int(count):
                print 'Document::checkDocument: book entry error (', count, ')', book.document_entry
                return False

            ## Check the current book
            elif book.checkBook() == False:
                print 'Document::checkDocument: book.checkBook failed'
                return False

            ## Increment book counter
            count = int(count + 1)
