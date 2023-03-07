# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:53:27 2023

@author: spk6f2
"""

import InventoryFunctions as IF


def main():
    IF.buildCreds()
    IF.retrieveBooksAndFlashCards()
    IF.retrieveCurrentStatus()
    IF.callMenu()


if __name__ == "__main__":
    main()