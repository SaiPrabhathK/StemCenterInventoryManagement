# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:49:52 2023

Legacy Code

@author: spk6f2
"""

# def checkOutItems(scannedList, checkedOutDetails):
#     """Main driver for Checking-out Items

#     Goes through the itemcodes in scannedList and determines their
#     spreadsheet ID and cell row & column to write new status in.

#     Parameters
#     ----------
#     scannedList : list
#         List of scanned item codes to be checked-out.
#     checkedOutDetails : string
#         String containing Name of the person checking out, date and
#         the expected return date (of all the items being checkout
#                                   - not individual items).

#     Returns
#     -------
#     None.

#     """
#     retrieveCurrentStatus()
#     listChange = True
#     for index, item in enumerate(scannedList):
#         sheetID = sheetSelector(item)
#         if (index > 0):
#             if (scannedList[index - 1][:2] != item[:2]):
#                 listChange = True
#             else:
#                 listChange = False
#         rangeName = rangeBuilder(item, listChange)
#         if sheetID is None:
#             print(
#                 f'Spreadsheet associated with item code "{item}" could not be found. Please check the code again.'
#             )
#             continue
#         if rangeName is None:
#             continue
#         if item in globals_.currentStatus['item']:
#             itemCountIndex = globals_.currentStatus['item'].index(item)
#             globals_.currentStatus['count'][itemCountIndex] += 1
#             updateValues(
#                 sheetID,
#                 rangeName,
#                 "USER_ENTERED",
#                 [["Checked out" + "\n" + checkedOutDetails]],
#             )
#         else:
#             globals_.currentStatus['item'].append(item)
#             globals_.currentStatus['count'].append(1)
#         updateCurrentStatus()
#     return

#


# def rangeBuilder(item, changeList):
#     """


#     Parameters
#     ----------
#     item : string
#         DESCRIPTION.

#     Returns
#     -------
#     string
#         DESCRIPTION.

#     """
#     if item.isnumeric():
#         if item in globals_.booksList:
#             sheetItemList = getValues(SHEETS["Books"]["SheetID"], "(B) Books" + "!A:A")
#             itemRowNumber = str(sheetItemList.index(item) + 1)
#             itemRowContents = getValues(
#                 SHEETS["Books"]["SheetID"],
#                 "(B) Books" + "!" + itemRowNumber + ":" + itemRowNumber,
#             )
#             itemColumnToBeInserted = len(itemRowContents)
#             return str(
#                 "(B) Books"
#                 + "!"
#                 + getSheetColumn(itemColumnToBeInserted, item)
#                 + str(globals_.booksList.index(item) + 1)
#             )
#         elif item in globals_.flashCardsList:
#             sheetItemList = getValues(
#                 SHEETS["Books"]["SheetID"], "(C) Flash Cards" + "!A:A"
#             )
#             itemRowNumber = str(sheetItemList.index(item) + 1)
#             itemRowContents = getValues(
#                 SHEETS["Books"]["SheetID"],
#                 "(C) Flash Cards" + "!" + itemRowNumber + ":" + itemRowNumber,
#             )
#             itemColumnToBeInserted = len(itemRowContents)
#             return str(
#                 "(C) Flash Cards"
#                 + "!"
#                 + getSheetColumn(itemColumnToBeInserted, item)
#                 + str(globals_.flashCardsList.index(item) + 1)
#             )
#     else:
#         itemCategory = getCategory(item)
#         if itemCategory == None:
#             return
#         sheetId = sheetSelector(item)
#         sheetTitle = getSheets(sheetId)["sheets"][itemCategory]["properties"]["title"]
#         if changeList:
#             globals_.sheetItemList = getValues(sheetId, sheetTitle + "!A:A")
#         if item not in globals_.sheetItemList:
#             print(
#                 f'The requested item code "{item}" could not be found. Please check the code again.'
#             )
#             return
#         itemRowNumber = str(globals_.sheetItemList.index(item) + 1)
#         itemRowContents = getValues(
#             sheetId, sheetTitle + "!" + itemRowNumber + ":" + itemRowNumber
#         )
#         itemColumnToBeInserted = len(itemRowContents)
#         return str(
#             sheetTitle
#             + "!"
#             + getSheetColumn(itemColumnToBeInserted, item)
#             + itemRowNumber
#         )
