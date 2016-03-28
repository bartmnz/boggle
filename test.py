#!/usr/bin/python

#stackoverflow.com/questions/4465052

import sys
req_version = (3,5)
cur_version = sys.version_info

if cur_version >= req_version:
    import gui
    gui.main()
else:
    print ("Upgrade your python!!")
