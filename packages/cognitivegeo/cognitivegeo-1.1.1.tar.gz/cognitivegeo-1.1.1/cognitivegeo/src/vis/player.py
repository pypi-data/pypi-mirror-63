#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Email:    geopy.info@gmail.com                                                            #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

# basic functions for player

import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.keyboard import keyboard as core_key


__all__ = ['player']


# List of all available player options, including Property, Key, and Interval
PlayerPropertyList = ['First', 'Previous', 'Backward', 'Pause', 'Forward', 'Next', 'Last', 'Interval']
PlayerKeyList = core_key.LetterKeyList
PlayerIntervalList = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]


class player:
    # Pack all functions as a class
    #
    PlayerPropertyList = PlayerPropertyList
    PlayerKeyList = PlayerKeyList
    PlayerIntervalList = PlayerIntervalList