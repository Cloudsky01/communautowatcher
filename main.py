import sys
import time
import webbrowser
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QListWidget, QSlider, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from logic import fetch_all_vehicles
from repeatTimer import RepeatTimer
from model import Model
from view import View
from controller import Controller


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    model = Model()
    controller = Controller(model, view)
    view.controller = controller
    view.model = model
    model.view = view
    view.show()
    sys.exit(app.exec_())