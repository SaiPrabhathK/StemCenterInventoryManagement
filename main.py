# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:53:27 2023

@author: spk6f2
"""

import InventoryFunctions as IF

# import globals_


def main():
    IF.buildCreds()
    IF.retrieveBooksAndFlashCards()
    IF.retrieveCurrentStatus()
    # print("Hello, Welcome to Inventory Management for STEM Center!")
    IF.callMenu()
    # callCheckOutItems(creds)
    # updateValues(sheetSelector(), rangeBuilder(), "USER_ENTERED", inputValues(), creds)
    # print(globals_.creds)
    # service = IF.build('sheets', 'v4', credentials=globals_.creds)
    # request = service.spreadsheets().get(spreadsheetId='1IoKPZoVo-kYQ_6f52tYYiQL4QezxsQaESX_aB0ynzB0')
    # response = request.execute()
    # print(response['sheets'][0]['properties']['title'])
    # IF.updateValues('10nw_zsCl9vwJxDV5_dE7kP6kuw7PUhJ2ycEhsvtJTzw', '(B) Books!D3', "USER_ENTERED", [['Hello, this is a test.', 'Test']])
    # print(IF.sheetSelector('l'))
    # print(IF.rangeBuilder('9780375867972'))
    # print(IF.updateValues('1IoKPZoVo-kYQ_6f52tYYiQL4QezxsQaESX_aB0ynzB0', '(T) Technology!D5', "USER_ENTERED", [['Checkedout']]))
    # globals_.currentStatus.append('Hello')
    # print(IF.updateValues(IF.SHEETS['CurrentStatus']['SheetID'], 'Checked Out List!A:A', "USER_ENTERED", [[item] for item in globals_.currentStatus]))
    # print(IF.updateValues(IF.SHEETS['CurrentStatus']['SheetID'], 'Checked Out List!A:A', "USER_ENTERED", [[''], ['']]))


if __name__ == "__main__":
    main()


# Storing all non zero values
# nonZeroValues = [x for x in arr if x != 0]

# Storing all zeroes
# zeroes = [j for j in arr if j == 0]

# Updating the answer
# arr = nonZeroValues + zeroes
