from PySide6 import QtCore, QtGui, QtWidgets
import sqlite3

class Connection(QtCore.QObject):
    signal = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

class LabelButton(QtWidgets.QLabel):
    def __init__(self, width, height, name, parent):
        super().__init__()
        self.setParent(parent)
        self.setText("<strong>"+name+"</strong>")
        self.setObjectName(name)
        self.connection = Connection()

    def mousePressEvent(self, event):
        self.connection.signal.emit(self.objectName())
