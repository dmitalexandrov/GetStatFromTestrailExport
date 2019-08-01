#https://pandas.pydata.org/pandas-docs/stable/user_guide
#https://khashtamov.com/ru/pandas-introduction/
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
            "Remove 's' char from Elapsed column, transform to Integer"
            "and Remove duplicates for total stat"
              .format(self.statTableClean["Case ID"].count()))
        self.statTableClean["Elapsed"] = self.statTableClean["Elapsed"].apply(
                                            lambda x: x.replace("s", ""))
        self.statTableClean["Elapsed"] = pandas.to_numeric(
                                            self.statTableClean["Elapsed"])
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
                            
    def getCountOfStatuses(self, status):
        return self.statTableClean[self.statTableClean["Status"] == 
                                            status.title()]["Case ID"].count()
    
    def getElapsedByStatus(self, status = "total"):
        if status.lower() == "total":
            return self.statTableClean["Elapsed"].sum() // 3600
        return self.statTableClean[self.statTableClean["Status"] == 
                                            status.title()]["Elapsed"].sum() // 3600

if __name__ == "__main__":
    ACTION_MENU = ("Please choose action:\n"
        "0: Exit\n"
        "1: Add file for stat\n"
        "2: Count uniq tests by types\n"
        "3: Elapsed stat\n")
    actionCode = input(ACTION_MENU)
    tables = dict()
    stop = True
    i = 0
    while stop:
        if actionCode is not "0":
            #add table from file to dict
            if actionCode is "1":
                result = GetTableFromFile()
                tables[i] = result
                i += 1
            #get stats
            if actionCode is "2":
                totalTable = pandas.DataFrame(index = [
                    #Type
                    "Automated",
                    "To be Automated",
                    "Manual Only",
                    "Total",
                    #Status
                    "Passed",
                    "Retest",
                    "Blocked",
                    "Failed"
                ])
                for key,value in tables.items(): 
                    totalTable[value.sourceFile] = [
                        #Type
                        value.getCountByType("Automated"),
                        value.getCountByType("To be Automated"),
                        value.getCountByType("Manual Only"),
                        value.getCountByType(),
                        #Status
                        value.getCountOfStatuses("Passed"),
                        value.getCountOfStatuses("Retest"),
                        value.getCountOfStatuses("Blocked"),
                        value.getCountOfStatuses("Failed")
                    ]
                    if key > 0:
                        totalTable["dif{}".format(key)] = \
                            totalTable.iloc[:,key] - totalTable.iloc[:,key-1]
                print(totalTable)
            if actionCode is "3":
                elapsedTable = pandas.DataFrame(index = [                    
                    #Elapsed
                    "Passed Elapsed",
                    "Retest Elapsed",
                    "Blocked Elapsed",
                    "Failed Elapsed",
                    "Total Elapsed"
                ])
                for key,value in tables.items(): 
                    elapsedTable[value.sourceFile] = [
                        #Elapsed
                        value.getElapsedByStatus("Passed"),
                        value.getElapsedByStatus("Retest"),
                        value.getElapsedByStatus("Blocked"),
                        value.getElapsedByStatus("Failed"),
                        value.getElapsedByStatus()
                    ]
                    if key > 0:
                        elapsedTable["dif{}".format(key)] = \
                            elapsedTable.iloc[:,key] - elapsedTable.iloc[:,key-1]
                print(elapsedTable)
            actionCode = input(ACTION_MENU)
        else:
            #exit
            stop = False