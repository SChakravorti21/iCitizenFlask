import re
import os
from distutils.sysconfig import get_python_lib


class DictFileMissingError(Exception):

    def __init__(self):
        self.message = "The dict file with this module is missing"

    def __str__(self):
        return self.message


class NotCorrectArgument(Exception):

    def __init__(self):
        self.message = "Argument provided is not of correct format"

    def __str__(self):
        return self.message


class Session:

    def __init__(self):
        """initializes session varaible"""
        self.session = []

    def addToSession(self, word):
        """Adds word to sessions object"""
        self.session.append(word.lower())

    def removeFromSession(self, word):
        """Removes word from sessions object"""
        for i in range(0, len(self.session)):
            if self.session[i] == word:
                del self.session[i]

    def addListToSession(self, sessionList):
        """adds entire list to session variable"""
        for word in sessionList:
            self.addToSession(word)


class Dictionary:

    def __init__(self, sessionObject=None):
        """defines some of its variables"""
        self.language = "en-US"
        self.sessionObject = sessionObject
        self.__dictionaryPath = get_python_lib()

    def isInDictionary(self, word):
        """Checks to see if the word is in the dictionary or not"""
        word = word.lower()
        try:
            fp = open(self.__dictionaryPath + os.sep + "dict.txt", "r")
        except IOError:
            raise DictFileMissingError
        else:
            flag = 0
            for line in fp:
                dword = line[:len(line) - 1]
                if dword == word:
                    flag = 1
            fp.close()
            if flag == 1:
                return True
            else:
                return False

    def isInSessionsDictionary(self, word):
        """Checks to see if the word is in the sessions added words"""
        word = word.lower()
        if self.sessionObject is not None:
            for sword in self.sessionObject.session:
                if sword == word:
                    return True
        return False

    def getSimilarWords(self, word):
        """Returns a list of words similar to the given word"""
        try:
            fp = open(self.__dictionaryPath + os.sep + "dict.txt", "r")
        except IOError:
            raise DictFileMissingError
        else:
            word = word.lower()
            # get different check patterns
            checkPatterns = []
            for i in range(0, len(word)):
                new_pattern = word[:i] + "." + word[i + 1:] + "\n"
                checkPatterns.append(new_pattern)
            matches = []
            listOfWords = ''
            for line in fp:
                listOfWords += line
            if self.sessionObject is not None:
                for line in self.sessionObject.session:
                    listOfWords += line + '\n'
            for pattern in checkPatterns:
                match = re.findall(pattern, listOfWords)
                temp = []
                for e in match:
                    e = e[:len(e) - 1]
                    if e not in matches and e not in temp \
                     and self.isInDictionary(e):
                        temp.append(e)
                matches += temp
            fp.close()
            return matches

    def changeSessionsDictionary(self, sessionObject):
        """Changes the session object with the new specified object"""
        self.sessionObject = sessionObject


def addToDictionary(word):
    """permanently adds words to dictionary file"""
    dictionaryPath = get_python_lib() + os.sep + "dict.txt"
    word = word.lower()
    try:
        fp = open(dictionaryPath, 'a')
    except IOError:
        raise DictFileMissingError
    else:
        fp.write(word + '\n')
        fp.close()
