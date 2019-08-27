#https://pandas.pydata.org/pandas-docs/stable/user_guide
#https://khashtamov.com/ru/pandas-introduction/
import pandas
import os
import sys

""" Get the statistic from Testrail export files
This script parse exported files from Testrail. For export
sould be selected columns:
- Case ID
- Elapsed
- Selenium Profile
- Status
- Type
additional install pandas, openpyxl
"""
class GetTableFromFile:
    statTableDirty = None
    statTableClean = None
    statTableUniqs = None
    sourceFile = None
    
    def __init__(self, fileName = ""):
        if fileName == "":
            self.sourceFile = self.__chooseFile()
        else:
            self.sourceFile = fileName
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
        print("Count of Case IDs before cleaning: {}"
        #    "Remove entires, where Elapsed is NULL"
              .format(self.statTableClean["Case ID"].count()))                
        self.statTableClean = self.statTableClean[
            self.statTableClean["Elapsed"].notnull()]

        print("Count of Case IDs after cleaning: {}"
            #"Remove 's' char from Elapsed column, transform to Integer"
            #"and Remove duplicates for total stat"
              .format(self.statTableClean["Case ID"].count()))
        self.statTableClean["Elapsed"] = self.statTableClean["Elapsed"].apply(
                                            lambda x: x.replace("s", ""))
        self.statTableClean["Elapsed"] = pandas.to_numeric(
                                            self.statTableClean["Elapsed"])
        #prevent SettingWithCopyWarning is displayed
        self.statTableUniqs = self.statTableClean.copy()
        self.statTableUniqs.drop_duplicates(subset = "Case ID", 
                                            keep = "last", inplace = True)

        print("Count of Case IDs after remove duplicates: {}"
              .format(self.statTableUniqs["Case ID"].count()))

    def __getCountByType(self, type = "total"):
        #print("Get count of {} tests".format(type.title()))
        if type.lower() == "total":
            return self.statTableUniqs["Case ID"].count()
        else:
            return self.statTableUniqs[self.statTableUniqs["Type"] == 
                                            type.title()]["Case ID"].count()
                            
    def __getCountOfStatuses(self, status):
        return self.statTableClean[self.statTableClean["Status"] == 
            status.title()]["Case ID"].count()
    
    def __getElapsedByStatus(self, type, status):
        if status.lower() == "total":
            return round(self.statTableClean[self.statTableClean["Type"] == 
                type]["Elapsed"].sum() / 3600, 2)
        #Use () for removing 'boolean series key will be reindexed to match dataframe index' warning
        return round(self.statTableClean[(self.statTableClean["Type"] == 
            type) & (self.statTableClean["Status"] == 
            status.title())]["Elapsed"].sum() / 3600, 2)

    def __getAverage(self, type):
        return round(self.statTableClean[self.statTableClean["Type"] == 
            type]["Elapsed"].mean() / 60, 2)

    def getTotalArray(self):
        return [
        #Type
            self.__getCountByType("Automated"),
            self.__getCountByType("To be Automated"),
            self.__getCountByType("Manual Only"),
            self.__getCountByType(),
            #Status
            self.__getCountOfStatuses("Passed"),
            self.__getCountOfStatuses("Retest"),
            self.__getCountOfStatuses("Blocked"),
            self.__getCountOfStatuses("Failed")
        ]

    def getElapsedArray(self, type):
        return [
            #Elapsed
            self.__getElapsedByStatus(type, "Passed"),
            self.__getElapsedByStatus(type, "Retest"),
            self.__getElapsedByStatus(type, "Blocked"),
            self.__getElapsedByStatus(type, "Failed"),
            self.__getElapsedByStatus(type, "Total")
        ]

    def getAverageArray(self, type):
        return [self.__getAverage(type)]

if __name__ == "__main__":
    ACTION_MENU_START = ("Please choose action:\n"
        "0: Exit\n"
        "1: Add file for stat\n"
        "2: Add all neighbours files\n")
    ACTION_MENU = ("Please choose action:\n"
        "0: Exit\n"
        "1: Add file for stat\n"
        "2: Add all neighbours files\n"
        "3: Count uniq tests by types\n"
        "4: Elapsed stat\n"
        "5: Write to file\n")
    actionCode = input(ACTION_MENU_START)
    tables = dict()
    stop = True
    i = 0
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
    elapsedAutomatedTable = pandas.DataFrame(index = [                    
        #Elapsed
        "Passed Elapsed (h)",
        "Retest Elapsed (h)",
        "Blocked Elapsed (h)",
        "Failed Elapsed (h)",
        "Total Elapsed (h)"
    ])
    elapsedNonAutomatedTable = pandas.DataFrame(index = [                    
        #Elapsed
        "Passed Elapsed (h)",
        "Retest Elapsed (h)",
        "Blocked Elapsed (h)",
        "Failed Elapsed (h)",
        "Total Elapsed (h)"
    ])
    elapsedTotalTable = pandas.DataFrame(index = [                    
        #Elapsed
        "Passed Elapsed (h)",
        "Retest Elapsed (h)",
        "Blocked Elapsed (h)",
        "Failed Elapsed (h)",
        "Total Elapsed (h)"
    ])
    averageTable = pandas.DataFrame(index = [                    
        "Total mean value (m)",
        "Automated mean value (m)"
        ])
    while stop:
        if actionCode is not "0":
            #add table from file to dict
            if actionCode is "1":
                result = GetTableFromFile()
                tables[i] = result
                totalTable[result.sourceFile] = result.getTotalArray()
                ea = result.getElapsedArray("Automated")
                etba = result.getElapsedArray("To Be Automated") 
                emo = result.getElapsedArray("Manual Only")
                elapsedAutomatedTable[result.sourceFile] = ea
                elapsedNonAutomatedTable[result.sourceFile] = [x + y for x, y in zip(etba, emo)]
                elapsedTotalTable[result.sourceFile] = [x + y + z for x, y, z in zip(ea, etba, emo)]
                
                aa = result.getAverageArray("Automated")
                atba = result.getAverageArray("To Be Automated")
                amo = result.getAverageArray("Manual Only")
                averageTable[result.sourceFile] = [
                    round((x + y + z) / 3, 2) for x, y, z in zip(aa, atba, amo)] + aa
                i += 1
            if actionCode is "2":
                for each in os.listdir():
                    if os.path.isfile("./{}".format(each)) and ".csv" in each:
                        result = GetTableFromFile(each)
                        tables[i] = result
                        i += 1
                #fill total table
                ti = 1 #additional table indexer for difference columns
                for key,value in tables.items(): 
                    totalTable[value.sourceFile] = value.getTotalArray()
                    if key == 1:
                        totalTable["dif{}".format(key)] = \
                            totalTable.iloc[:,key] - totalTable.iloc[:,key-1]
                    elif key > 1:
                        print("{}({})".format(key, ti))
                        totalTable["dif{}".format(key)] = \
                            totalTable.iloc[:,key + ti] - totalTable.iloc[:,key + ti - 2]
                        ti += 1
                #fill elapsed table
                ei = 1 #additional table indexer for difference columns
                for key,value in tables.items():
                    ea = value.getElapsedArray("Automated")
                    etba = value.getElapsedArray("To Be Automated") 
                    emo = value.getElapsedArray("Manual Only")
                    elapsedAutomatedTable[value.sourceFile] = ea
                    elapsedNonAutomatedTable[value.sourceFile] = [x + y for x, y in zip(etba, emo)]
                    elapsedTotalTable[value.sourceFile] = [x + y + z for x, y, z in zip(ea, etba, emo)]

                    aa = value.getAverageArray("Automated")
                    atba = value.getAverageArray("To Be Automated")
                    amo = value.getAverageArray("Manual Only")
                    averageTable[value.sourceFile] = [
                        round((x + y + z) / 3, 2) for x, y, z in zip(aa, atba, amo)] + aa
                    if key == 1:
                        elapsedAutomatedTable["dif{}".format(key)] = \
                            elapsedAutomatedTable.iloc[:,key] - elapsedAutomatedTable.iloc[:,key-1]
                        elapsedNonAutomatedTable["dif{}".format(key)] = \
                            elapsedNonAutomatedTable.iloc[:,key] - elapsedNonAutomatedTable.iloc[:,key-1]
                        elapsedTotalTable["dif{}".format(key)] = \
                            elapsedTotalTable.iloc[:,key] - elapsedTotalTable.iloc[:,key-1]
                        averageTable["dif{}".format(key)] = \
                            averageTable.iloc[:,key] - averageTable.iloc[:,key-1]
                    elif key > 1:
                        elapsedAutomatedTable["dif{}".format(key)] = \
                            elapsedAutomatedTable.iloc[:,key + ei] - elapsedAutomatedTable.iloc[:,key + ei -2]
                        elapsedNonAutomatedTable["dif{}".format(key)] = \
                            elapsedNonAutomatedTable.iloc[:,key + ei] - elapsedNonAutomatedTable.iloc[:,key + ei -2]
                        elapsedTotalTable["dif{}".format(key)] = \
                            elapsedTotalTable.iloc[:,key + ei] - elapsedTotalTable.iloc[:,key + ei -2]
                        averageTable["dif{}".format(key)] = \
                            averageTable.iloc[:,key + ei] - averageTable.iloc[:,key + ei -2]
                        ei += 1
            
            if actionCode is "3":                
                print(totalTable)
            if actionCode is "4":
                print("Automated: \n {0}\n".format(elapsedAutomatedTable))
                print("NonAutomated: \n {0}\n".format(elapsedNonAutomatedTable))
                print("Total: \n {0}\n".format(elapsedTotalTable))
                print("Average: \n {0}\n".format(averageTable))
            if actionCode is "5":
                #totalTable.to_csv("./statTotal.csv", sep=",")
                #elapsedAutomatedTable.to_csv("./statElAuto.csv", sep=",")
                #elapsedNonAutomatedTable.to_csv("./statElNonAto.csv", sep=",")
                #elapsedTotalTable.to_csv("./statElTot.csv", sep=",")
                #averageTable.to_csv("./statAver.csv", sep=",")
                with pandas.ExcelWriter('./GSFT.xlsx') as writer:
                    totalTable.to_excel(writer, sheet_name="Total")
                    elapsedAutomatedTable.to_excel(writer, sheet_name="ElapsedAutomated")
                    elapsedNonAutomatedTable.to_excel(writer, sheet_name="ElapsedNonAutomated")
                    elapsedTotalTable.to_excel(writer, sheet_name="ElapsedTotal")
                    averageTable.to_excel(writer, sheet_name="Average")
            actionCode = input(ACTION_MENU)
        else:
            #exit
            sys.exit()