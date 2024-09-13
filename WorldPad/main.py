import sys
import os
import pickle
import sqlite3
from PySide6 import QtGui, QtCore, QtWidgets

import labelButton

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.dir = os.path.normpath("./Projects/")
        self.path = os.path.normpath("./Projects/projects.wpd")
        self.loadProjects()

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, parent=self)
        self.setWindowTitle("WorldPad")
        self.setGeometry(0, 0, 1920, 1080)
        self.displayTopElements()
        self.displayProjects()

    def closeEvent(self, event):
        msg = "Are you sure you want to quit?"
        input = QtWidgets.QMessageBox.question(self, 'Quit', msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if input == QtWidgets.QMessageBox.Yes:
            self.saveProjects()
            event.accept()
        else:
            event.ignore()

    def saveProjects(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        if not os.path.exists(self.path):
            nf = open(self.path, "xt")
            nf.close()

        proj = open(self.path, "wb")
        pickle.dump(self.projects, proj)
        proj.close()

    def loadProjects(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        if not os.path.exists(self.path):
            nf = open(self.path, "xt")
            nf.close()

        proj = open(self.path, "rb")
        if os.path.getsize(self.path) > 0:
            self.projects = pickle.load(proj)
            if self.projects == None:
                self.projects = dict()
        else:
            self.projects = dict()

        proj.close()

    def displayTopElements(self):
        text = QtWidgets.QLabel("<h1>WorldPad Hub</h1>", parent=self)
        self.layout.addWidget(text)
        self.update()

    def displayProjects(self):
        #row = 0
        #col = 0

        for pname in self.projects.keys():
            square = QtWidgets.QLabel(parent=self)
            pixmap = QtGui.QPixmap(240, 240)
            pixmap.fill(QtGui.QColor("green"))
            square.setPixmap(pixmap)
            text = labelButton.LabelButton(240, 240, pname, self)
            text.connection.signal.connect(self.projectLabelClick)
            self.layout.addWidget(square)
            self.layout.addWidget(text)

            #col += 1
            #if col > 3:
            #    col = 0
            #    row += 1

        addProj = QtWidgets.QLabel(parent=self)
        pixmap = QtGui.QPixmap(240, 240)
        pixmap.fill(QtGui.QColor("white"))
        addProj.setPixmap(pixmap)
        addText = labelButton.LabelButton(240, 240, "Add Project", self)
        addText.connection.signal.connect(self.addProjectClick)
        self.layout.addWidget(addProj)
        self.layout.addWidget(addText)

        self.update()

    def clearWidgets(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        self.update()


    def projectLabelClick(self, name):
        projDB = self.projects.get(name)

        #options = QtWidgets.QDialogButtonBox(parent=self)
        #options.addButton("Open Project", QtWidgets.QDialogButtonBox.AcceptRole)
        #options.addButton("Delete Project", QtWidgets.QDialogButtonBox.DestructiveRole)
        #options.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        #options.show()

        msg = "Delete project?"
        input = QtWidgets.QMessageBox.question(self, 'Delete', msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if input == QtWidgets.QMessageBox.Yes:
            self.projects.pop(name)
            if os.path.exists(name + ".db"):
                os.remove(name + ".db")

            self.clearWidgets()
            self.displayTopElements()
            self.displayProjects()

    def addProjectClick(self, text):
        name, status = QtWidgets.QInputDialog.getText(self, "New Project", "Enter Project Name:")
        if name and status and name not in self.projects:
            db = sqlite3.connect(name + ".db")
            self.projects[name] = name + ".db"
            self.clearWidgets()
            self.displayTopElements()
            self.displayProjects()

def launchGUI(argv):
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launchGUI(sys.argv)
