# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:54:21 2023

@author: spk6f2

This module contains all the functions and objects required for the application.
"""

from __future__ import print_function

import os.path
import sys
import string
import subprocess
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import globals_

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Update the values in the following three objects (SHEETS --> dict,
# generalCategories --> list and cPLTWCategories --> list)
SHEETS = {
    "Books": {
        "SheetID": "10nw_zsCl9vwJxDV5_dE7kP6kuw7PUhJ2ycEhsvtJTzw",
        "SheetName": "Books Inventory",
    },
    "General": {
        "SheetID": "1IoKPZoVo-kYQ_6f52tYYiQL4QezxsQaESX_aB0ynzB0",
        "SheetName": "General Inventory",
    },
    "PLTW": {
        "SheetID": "1UeB6x-LYNOcEETpTAvMH1rJtQod5z9vYeZCwRZdbjSA",
        "SheetName": "PLTW Inventory",
    },
    "CurrentStatus": {
        "SheetID": "1PYXzaxsv728UCDJWNyXZuvDujVL49owZNAeVCshMC4M",
        "SheetName": "Current Status",
    },
}

generalCategories = ["GT", "GM", "GJ", "GR", "GE", "GO", "GG", "GP"]

PLTWCategories = ["PL", "PG", "PB", "PC", "PE"]

def resourcePath(relativePath):
    """Get absolute path to resource, works for dev and for PyInstaller.
    
    Keyword arguments:
        relativePath -- most often the name of the file.
    
    Fix found on stack overflow to work with exe generated by pyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

def retrieveCurrentStatus():
    """Retrieves currently checked-out itemlist.
    
    Updates currentStatus object in globals_ module.
    
    Returns
    -------
    None.

    """
    globals_.currentStatus = getValues(
        SHEETS["CurrentStatus"]["SheetID"], "Checked Out List!A:A"
    )


def checkAndUpdateCurrentStatus(item):
    """Checks to see if the item had already been checked-out or not.
    

    Parameters
    ----------
    item : itemcode
        Itemcode can be an integer or alphnumeric string starting 
        with two characters denoting the item category.

    Returns
    -------
    bool
        True if item already checked-out. False otherwise.

    """
    if item in globals_.currentStatus:
        return True
    else:
        return False


def getSheetColumn(itemColumnToBeInserted, item):
    """Computes the column alphabet, new data is to be entered in.
    

    Parameters
    ----------
    itemColumnToBeInserted : integer
        This is the no. of data cells in the row of the item.
    item : itemcode
        Itemcode can be an integer or alphnumeric string starting 
        with two characters denoting the item category.

    Returns
    -------
    letter : One alphabet from string.ascii_uppercase
        This alphabet represents a column in the spreadsheet.

    """
    num = itemColumnToBeInserted
    letter = ""
    if num < 26:
        letter = string.ascii_uppercase[num]
    elif num < 702:

        letter = (
            string.ascii_uppercase[int(num / 26) - 1]
            + string.ascii_uppercase[int(num % 26)]
        )
    else:
        if (18278 - num) < 4:
            print(
                f"Consider creating a new sheet. There are only {18278-num} cells available in the sheet for {item}."
            )
        letter = str(
            string.ascii_uppercase[int(((num - 26) / 676) - 1)]
            + string.ascii_uppercase[int(num % 676 / 26) - 1]
            + string.ascii_uppercase[int(num % 26)]
        )
        # while num > 25:
        #   num = num - 25
        #  letter = letter + string.ascii_uppercase[num - 1]
    return letter


def buildCreds():
    # global creds
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(resourcePath("token.json")):
        creds = Credentials.from_authorized_user_file(resourcePath("token.json"), SCOPES)
        # print(creds)
        globals_.creds = creds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(resourcePath("credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(resourcePath("token.json"), "w") as token:
            token.write(creds.to_json())
        globals_.creds = creds


def updateCurrentStatus():
    values = globals_.currentStatus
    values = [[item] for item in values]
    updateValues(
        SHEETS["CurrentStatus"]["SheetID"],
        "Checked Out List!A:A",
        "USER_ENTERED",
        values,
    )


def updateValues(spreadsheet_id, range_name, value_input_option, _values):
    try:

        service = build("sheets", "v4", credentials=globals_.creds, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
        # type(_values) - list of lists
        body = {"values": _values}
        # if spreadsheet_id == '':
        #   raise ValueError('No spreadsheet found for the item')
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        # return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def getValues(spreadsheet_id, range_name):
    try:
        service = build("sheets", "v4", credentials=globals_.creds, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        #flatten the result into list of elements.
        flatList = [element for innerList in result["values"] for element in innerList]
        #flatten the result into list of list elements.
        flatList2 = [element for element in result["values"]]
        return flatList
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
        # research more about os.execv later


def sheetSelector(item):
    if item.isnumeric():
        return SHEETS["Books"]["SheetID"]
    elif item[:2] in generalCategories:
        return SHEETS["General"]["SheetID"]
    elif item[:2] in PLTWCategories:
        return SHEETS["PLTW"]["SheetID"]
    else:
        print("Unidentified item code: ", item)
        return


# Gets the titles of all the sheets in a spreadsheet
def getSheets(sheetId):
    try:
        service = build("sheets", "v4", credentials=globals_.creds, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
        request = service.spreadsheets().get(spreadsheetId=sheetId)
        response = request.execute()
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def getCategory(item):
    category = item[:2]
    if category in generalCategories:
        return generalCategories.index(category)
    elif category in PLTWCategories:
        return PLTWCategories.index(category)
    else:
        return


def rangeBuilder(item):
    if item.isnumeric():
        if item in globals_.booksList:
            sheetItemList = getValues(SHEETS["Books"]["SheetID"], "(B) Books" + "!A:A")
            itemRowNumber = str(sheetItemList.index(item) + 1)
            itemRowContents = getValues(
                SHEETS["Books"]["SheetID"],
                "(B) Books" + "!" + itemRowNumber + ":" + itemRowNumber,
            )
            itemColumnToBeInserted = len(itemRowContents)
            return str(
                "(B) Books"
                + "!"
                + getSheetColumn(itemColumnToBeInserted, item)
                + str(globals_.booksList.index(item) + 1)
            )
        elif item in globals_.flashCardsList:
            sheetItemList = getValues(
                SHEETS["Books"]["SheetID"], "(C) Flash Cards" + "!A:A"
            )
            itemRowNumber = str(sheetItemList.index(item) + 1)
            itemRowContents = getValues(
                SHEETS["Books"]["SheetID"],
                "(C) Flash Cards" + "!" + itemRowNumber + ":" + itemRowNumber,
            )
            itemColumnToBeInserted = len(itemRowContents)
            return str(
                "(C) Flash Cards"
                + "!"
                + getSheetColumn(itemColumnToBeInserted, item)
                + str(globals_.flashCardsList.index(item) + 1)
            )
    else:
        itemCategory = getCategory(item)
        if itemCategory == None:
            return
        sheetId = sheetSelector(item)
        sheetTitle = getSheets(sheetId)["sheets"][itemCategory]["properties"]["title"]
        sheetItemList = getValues(sheetId, sheetTitle + "!A:A")
        if item not in sheetItemList:
            print(
                f'The requested item code "{item}" could not be found. Please check the code again.'
            )
            return
        itemRowNumber = str(sheetItemList.index(item) + 1)
        itemRowContents = getValues(
            sheetId, sheetTitle + "!" + itemRowNumber + ":" + itemRowNumber
        )
        itemColumnToBeInserted = len(itemRowContents)
        return str(
            sheetTitle
            + "!"
            + getSheetColumn(itemColumnToBeInserted, item)
            + itemRowNumber
        )


def checkInItems(scannedList, checkedInDetails):
    retrieveCurrentStatus()
    for item in scannedList:
        sheetID = sheetSelector(item)
        rangeName = rangeBuilder(item)
        if sheetID is None:
            print(
                f'Spreadsheet associated with item code "{item}" could not be found. Please the check code again.'
            )
            continue
        if rangeName is None:
            continue
        if checkAndUpdateCurrentStatus(item):
            updateValues(
                sheetID,
                rangeName,
                "USER_ENTERED",
                [["Checked In" + "\n" + checkedInDetails]],
            )
            globals_.currentStatus.remove(item)
            globals_.currentStatus.append("")
            # globals_.currentStatus[globals_.currentStatus.index(item)+1] = str('')
            updateCurrentStatus()
        else:
            print(
                f'This item: {item} is already "Checkedin". \nPlease make sure you have selected the right option for this item.'
            )
    return


def checkOutItems(scannedList, checkedOutDetails):
    retrieveCurrentStatus()
    for item in scannedList:
        sheetID = sheetSelector(item)
        rangeName = rangeBuilder(item)
        if sheetID is None:
            print(
                f'Spreadsheet associated with item code "{item}" could not be found. Please check the code again.'
            )
            continue
        if rangeName is None:
            continue
        if item in globals_.currentStatus:
            print(
                f'This item: {item} is already "Checkedout".\nPlease check-in the item before checking it out or make sure you have selected the right option for this item.'
            )
        else:
            updateValues(
                sheetID,
                rangeName,
                "USER_ENTERED",
                [["Checked out" + "\n" + checkedOutDetails]],
            )
            globals_.currentStatus.append(item)
            updateCurrentStatus()
    return


def callCheckOutItems():
    scannedList = []
    print("Enter '0' (zero) to cancel ||  '1' to finish after scanning\n")
    print("Scan the items to be checked out")
    while True:
        newScan = input("--> ")
        if newScan == "0":
            break
        elif newScan == "1":
            if len(scannedList) > 0:
                details = input("Who's checking out? --> ")
                if details == "0":
                    break
                details = "Checked out by: " + details
                expectedReturn = input("Enter expected return date --> ")
                if expectedReturn == "0":
                    break
                expectedReturn = "Expected return: "
                currentTime = datetime.now()
                checkedOutTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")
                checkedOutDetails = (
                    details
                    + ",\n"
                    + expectedReturn
                    + ",\n"
                    + "Checked out at: "
                    + checkedOutTime
                )
                checkOutItems(scannedList, checkedOutDetails)
                return
            else:
                break
        else:
            scannedList.append(newScan)
    return


def callCheckInItems():
    scannedList = []
    print("/nEnter '0' (zero) to cancel ||  '1' to finish after scanning\n")
    print("Scan the items to be checked in")
    while True:
        newScan = input("--> ")
        if newScan == "0":
            break
        elif newScan == "1":
            if len(scannedList) > 0:
                details = input("Who's checking in? --> ")
                if details == "0":
                    break
                details = "Checked in by: " + details
                currentTime = datetime.now()
                checkedInTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")
                checkedInDetails = details + ",\n" + "Checked in at: " + checkedInTime
                checkInItems(scannedList, checkedInDetails)
                return
            else:
                break
        else:
            scannedList.append(newScan)
    return


def callGetStatus():
    pass


def callMenu():
    while True:
        print("\nWhat would you like to do?")
        print("1. Check-out Items (Requires scanning items)")
        print("2. Check-in Items (Requires scanning items)")
        print("3. Get Item(s) Status (Not implemented yet)")
        print("4. Quit Program!")
        print("5. Clear Screen")
        print("6. Update this Application")
        menuOptionInput = str(input("Enter the action you want to perform --> "))
        if menuOptionInput == "1":
            callCheckOutItems()
            # updateSheets(action='checkout')
        elif menuOptionInput == "2":
            callCheckInItems()
            # updateSheets(action='checkin')
        elif menuOptionInput == "3":
            callGetStatus()
        elif menuOptionInput == "4":
            print("\nYou have exited the Inventory Management Program!")
            sys.exit()
        elif menuOptionInput == "5":
            os.system('cls')
        elif menuOptionInput == "6":
            scriptPath = resourcePath("callUpdate.ps1")
            p = subprocess.Popen(["powershell.exe", scriptPath], stdout=sys.stdout)
            p.communicate()
        else:
            print("\nEnter the correct option")


def retrieveBooksAndFlashCards():
    globals_.booksList = getValues(SHEETS["Books"]["SheetID"], "(B) Books!A:A")
    globals_.flashCardsList = getValues(
        SHEETS["Books"]["SheetID"], "(C) Flash Cards!A:A"
    )
