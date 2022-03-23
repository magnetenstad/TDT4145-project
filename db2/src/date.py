from datetime import date
from msilib.schema import Error

class Date:

    def __init__(self, date):
        try:
            self.validate(date)
            self.date = date
        except :
            print(Exception)


    def validate(date):
        dateList = date.split('.')
        today = date.today().strftime("%d/%m/%Y").split('/')
        for d in dateList:
            if not d.isnumeric():
                raise Exception("Ugyldig dato")

        if (len(dateList[0]) != 4) or (len(dateList[1]) != 2) or (len(dateList[2]) != 2) or dateList[1] > 12:
            raise Exception("Ugyldig dato")
        if dateList[1] == 