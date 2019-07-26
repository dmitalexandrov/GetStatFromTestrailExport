#https://pandas.pydata.org/pandas-docs/stable/user_guide
#realpython.com/python-csv/
#habr.com/ru/post/196980/
#khashtamov.com/ru/pandas-introduction/
import pandas
import os

class GetTableFromFile:

    def parseFile(self, fileName):
        if os.path.isfile("./{0}".format(fileName)):
            self.df = pandas.read_csv(fileName, sep=",", header=1)
        else:
            print("Filename is incorrect")


if __name__ == "__main__":
    statTable = GetTableFromFile()
    statTable.parseFile("sprint_66_regression_suite.csv")
    print(statTable.df[statTable.df["Case ID"] == "C31294"])