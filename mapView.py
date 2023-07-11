from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QGridLayout, QLabel, QComboBox, QCheckBox, QGroupBox, QScrollArea, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QListView, QAbstractItemView, QListWidget, QListWidgetItem
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

class MapWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.init_map()

    def update_map(self):
        pass

    def init_map(self, lat=45.54, lng=-73.59):
        self.m = folium.Map(location=(lat, lng), tiles="cartodb positron")

        self.webEngineView = QWebEngineView()
        self.webEngineView.load(QUrl.fromLocalFile(QFileInfo("./map/map.html").absoluteFilePath()))

        layout = QVBoxLayout()
        layout.addWidget(self.webEngineView)
        self.setLayout(layout)

    def add_marker(self, lat, lng, popup):
        folium.Marker(location=(lat, lng), popup=popup).add_to(self.m)

    def save_map(self):
        self.m.save("./map/map.html")