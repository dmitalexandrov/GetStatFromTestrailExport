#https://pandas.pydata.org/pandas-docs/stable/user_guide
#realpython.com/python-csv/
#habr.com/ru/post/196980/
#khashtamov.com/ru/pandas-introduction/
#1.суммарное количество тестов по типам и всего
#2. суммарное время:
#	- всего прогона
#	- всех тестов по типам
#3. количество запусков по типам
import pandas
import os


class GetTableFromFile:
    statTable = None
    sourceFile = None

    def __init__(self):
        self.sourceFile = self.__chooseFile()

    def __chooseFile(self):
        fileList = dict()
        i = 0
        for each in os.listdir():
            if os.path.isfile("./{}".format(each)) and ".csv" in each:
                fileList[str(i)] = each
                print("{0}: {1}".format(i, each))
                i += 1
        fileCode = input("Please select file:")
        stop = True
        while stop:
            if fileCode not in fileList:
                fileCode = input("Please select file:")
            else:
                stop = False
        return fileList[fileCode]

    def _parseFile(self, fileName = None):
        if fileName is None:
            fileName = self.sourceFile
        if os.path.isfile("./{0}".format(fileName)):
             self.statTable = pandas.read_csv(fileName, sep=",", header=1)
        else:
            print("Filename is incorrect")

    def getCountByType(self, type):
        

if __name__ == "__main__":
    file = GetTableFromFile.chooseFile()
    statTable = GetTableFromFile.parseFile(file)    
    print(statTable[statTable["Case ID"] == "C31294"])