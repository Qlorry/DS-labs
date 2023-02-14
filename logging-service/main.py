import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from LoggingApp import LoggingApp

if __name__ == '__main__':
    app = LoggingApp()
    app.run()