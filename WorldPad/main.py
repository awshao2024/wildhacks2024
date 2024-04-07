import sys
import os
import pickle
import sqlite3
import PySide6.QtWidgets as QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.dir = os.path.normpath("./Projects/")
        self.path = os.path.normpath("./Projects/projects.wpd")
        self.projects = self.loadProjects()

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
        else:
            self.projects = {}
        proj.close()


def launchGUI(argv):
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.setWindowTitle("WorldPad")
    window.setGeometry(0, 0, 1920, 1080)
    text = QtWidgets.QLabel("<h1>WorldPad Hub</h1>", parent=window)
    text.move(60, 15)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launchGUI(sys.argv)
