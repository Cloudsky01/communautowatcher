from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QGridLayout, QLabel, QComboBox, QCheckBox, QGroupBox, QScrollArea, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QListView, QAbstractItemView, QListWidget, QListWidgetItem
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

from mapView import MapWidget


class myListWidget(QListWidget):
   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

class StationsWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.refresh_thread = None
        self.stop_flag = False

        self.model = model

        self.listWidget = myListWidget()
        self.listWidget.itemClicked.connect(self.listWidget.Clicked)

        self.refresh_stations()

        self.mapWidget = MapWidget(self.model)
        self.add_stations_marker()
        self.mapWidget.save_map()        

        layout = QVBoxLayout()
        layout.addWidget(self.mapWidget)
        layout.addWidget(self.listWidget)
        self.setLayout(layout)
        self.show()

    def refresh_stations(self):
        self.model.refresh_stations()
        self.update_stations()

    def update_stations(self):
        self.stations = self.model.get_stations()
        for station in self.stations:
            self.listWidget.addItem(str(station))
        
    def add_stations_marker(self):
        self.stations = self.model.get_stations()
        for station in self.stations:
            self.mapWidget.add_marker(station['location']['latitude'], station['location']['longitude'], station['stationName'])



        

        