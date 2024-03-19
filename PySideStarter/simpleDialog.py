#!/usr/bin/env python
import sys
from PySide2 import QtCore,QtWidgets



class SimpleDialog(QtWidgets.QDialog) :
  def __init__(self,parent=None) :
    super(SimpleDialog,self).__init__(parent)
    self.setWindowTitle("Simple Dialog")
    self.setMinimumWidth(200)
    

if __name__ == "__main__" :
  app = QtWidgets.QApplication(sys.argv)

  dialog=SimpleDialog()
  dialog.show()
  app.exec_()
