# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:53:27 2023

@author: spk6f2

The main driver code that calls functions to initialize globals
and launches the Main menu by calling callMenu() from InventoryFunctions 
module
"""

import InventoryFunctions as IF


def main():
    """
    

    Returns
    -------
    None.

    """
    IF.buildCreds()
    #print(IF.getValues(IF.SHEETS["Books"]["SheetID"], "(B) Books!A:B"))
    #IF.updateValues("10nw_zsCl9vwJxDV5_dE7kP6kuw7PUhJ2ycEhsvtJTzw", "(B) Books!D2", "USER_ENTERED", [["Hello"]])
    IF.retrieveBooksAndFlashCards()
    IF.retrieveCurrentStatus()
#    IF.updateCurrentStatus()
    #print(IF.globals_.flashCardsList)
    IF.callMenu()


if __name__ == "__main__":
    main()