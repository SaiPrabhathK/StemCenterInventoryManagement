# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 17:43:15 2023

@author: spk6f2
"""

import string

num = 0
while True:
    num = num + int(input("Enter a number:"))
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
                f"Consider creating a new sheet. There are only {18278-num} cells available in the sheet."
            )
        letter = (
            string.ascii_uppercase[int(((num - 26) / 676) - 1)]
            + string.ascii_uppercase[int(num % 676 / 26) - 1]
            + string.ascii_uppercase[int(num % 26)]
        )
        # while num > 25:
        #   num = num - 25
        #  letter = letter + string.ascii_uppercase[num - 1]
    print(num, letter)
