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
    IF.retrieveBooksAndFlashCards()
    IF.retrieveCurrentStatus()
    IF.callMenu()


if __name__ == "__main__":
    main()
