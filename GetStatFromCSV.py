#https://pandas.pydata.org/pandas-docs/stable/user_guide
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
#https://pythonworld.ru/obrabotka-dannyx/pandas-cookbook-1-csv-reading.html
#https://khashtamov.com/ru/pandas-introduction/
#https://ru.stackoverflow.com/questions/896180/%D0%98%D0%B7%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C-%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-dataframe-pandas-%D0%BF%D0%BE-%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8E

#1. get file
#2. get dirty table from file
#3. remove empty duplicates (where Elapsed is null)
#4. 
import pandas
import os


class GetTableFromFile:
    statTableDirty = None
    statTableClean = None
    statTableUniqs = None
    sourceFile = None
    
    def __init__(self):
        self.sourceFile = self.__chooseFile()        
        self._parseFile()
        self._cleanTable()

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
            print("Using default file")
            fileName = self.sourceFile
        if os.path.isfile("./{0}".format(fileName)):
             self.statTableDirty = pandas.read_csv(fileName, sep=",",
                header=1)
        else:
            print("Filename is incorrect")

    def _cleanTable(self):
        #prevent SettingWithCopyWarning is displayed
        #https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
        self.statTableClean = self.statTableDirty.copy()
        print("Count of Case IDs before cleaning is \n{} \n"
            "Remove entires, where Elapsed is NULL"
              .format(self.statTableClean["Case ID"].count()))                
        self.statTableClean = self.statTableClean[
            self.statTableClean["Elapsed"].notnull()]

        print("Count of Case IDs after cleaning is \n{} \n"
            "Remove 's' char from Elapsed column and Remove duplicates for total stat"
              .format(self.statTableClean["Case ID"].count()))
        self.statTableClean["Elapsed"] = self.statTableClean["Elapsed"].apply(
                                            lambda x: x.replace("s", ""))
        #prevent SettingWithCopyWarning is displayed
        self.statTableUniqs = self.statTableClean.copy()
        self.statTableUniqs.drop_duplicates(subset = "Case ID", 
                                            keep = "last", inplace = True)

        print("Count of Case IDs after remove duplicates \n{}"
              .format(self.statTableUniqs["Case ID"].count()))

    def getCountByType(self, type = "total"):
        #print("Get count of {} tests".format(type.title()))
        if type.lower() == "total":
            return self.statTableUniqs["Case ID"].count()
        else:
            return self.statTableUniqs[self.statTableUniqs["Type"] == 
                                            type.title()]["Case ID"].count()

if __name__ == "__main__":
    ACTION_MENU = ("Please choose action:\n"
        "0: Exit\n"
        "1: Add file for stat"
        "2: Count uniq tests by types\n")
    actionCode = input(ACTION_MENU)
    tables = dict()
    stop = True
    while stop:
        if actionCode is not "0":
            if actionCode is "1":
                result = GetTableFromFile()
                tables[result.sourceFile] = result
            if actionCode is "2":
                totalTable = pandas.DataFrame({})
                for each in tables:
                    https://stackoverflow.com/questions/28056171/how-to-build-and-fill-pandas-dataframe-from-for-loop
                print(self.getCountByType())
                print(self.getCountByType("Automated"))
                print(self.getCountByType("To be Automated"))
                print(self.getCountByType("Manual Only"))
            actionCode = input(self.ACTION_MENU)
        else:
            stop = False