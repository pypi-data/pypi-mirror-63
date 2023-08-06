'''
 Copyright (c) 2020, UChicago Argonne, LLC
 See LICENSE file.
'''
import sys
import PyQt5.QtWidgets as qtWidgets
from minixs.gui.qtevaluator.evaluatormainwindow import EvaluatorMainWindow

def main():
    
    app = qtWidgets.QApplication(sys.argv)
    mainWindow = EvaluatorMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())