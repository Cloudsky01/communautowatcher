import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QListWidgetItem,  QWidget, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QListWidget, QSlider, QMessageBox, QTabWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

from api import fetch_all_vehicles, fetch_vehicle_details
from model import Model
from repeatTimer import RepeatTimer
from utils import openURL

class CustomListWidget(QListWidget):
    itemClicked = pyqtSignal(QListWidgetItem)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            self.itemClicked.emit(item)
        super().mousePressEvent(event)


class CustomListItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__(text)


class FilterWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the CustomListWidget
        self.list_widget = CustomListWidget()

        # Create the filter line edit for make of the vehicle
        self.make_filter_edit = QLineEdit()
        self.make_filter_edit.setPlaceholderText("Enter make of the vehicle")

        # Create the filter line edit for distance
        self.distance_filter_edit = QLineEdit()
        self.distance_filter_edit.setPlaceholderText("Enter distance")

        # Create the filter buttons
        self.make_filter_button = QPushButton("Filter by Make")
        self.distance_filter_button = QPushButton("Filter by Distance")

        # Connect the filter buttons to their respective slots
        self.make_filter_button.clicked.connect(self.filter_by_make)
        self.distance_filter_button.clicked.connect(self.filter_by_distance)

        # Create a layout and add the widgets
        layout = QVBoxLayout()
        layout.addWidget(self.make_filter_edit)
        layout.addWidget(self.make_filter_button)
        layout.addWidget(self.distance_filter_edit)
        layout.addWidget(self.distance_filter_button)
        layout.addWidget(self.list_widget)

        # Set the layout for the widget
        self.setLayout(layout)

    def create_list_item(self, text):
        item = CustomListItem(text)
        item.setFlags(item.flags() | Qt.ItemIsSelectable)
        item.setFlags(item.flags() | Qt.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignCenter)
        item.setCheckState(Qt.Unchecked)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        return item

    def update_vehicle_list(self, vehicle_info_list):
        self.clear_list()  # Clear the list before populating with new items
        for vehicle_info in vehicle_info_list:
            self.add_item(str(vehicle_info))  # Convert vehicle_info to a string and add it as an item

    def add_item(self, text):
        item = self.create_list_item(text)
        self.list_widget.addItem(item)

    def clear_list(self):
        self.list_widget.clear()

    def clear(self):
        self.clear_list()

    def filter_by_make(self):
        make_filter_text = self.make_filter_edit.text()
        # Apply filter by make logic
        # Clear the list_widget and populate it with filtered items

    def filter_by_distance(self):
        distance_filter_text = self.distance_filter_edit.text()
        # Apply filter by distance logic
        # Clear the list_widget and populate it with filtered items


class CustomWidget(QWidget):
    def __init__(self, model: Model):
        super().__init__()

        self.refresh_thread = None
        self.stop_flag = False

        self.model = model

        self.distance_label = QLabel()
        self.distance_slider = QSlider(Qt.Horizontal)
        self.distance_slider.setRange(1, 1000)
        self.distance_slider.setValue(100)
        self.distance_slider.valueChanged.connect(self.on_distance_slider_changed)

        self.refresh_interval_input = QLineEdit()

        self.sleep_time_input = QLineEdit()

        self.longitude_input = QLineEdit()

        self.latitude_input = QLineEdit()

        self.openCommunautoButton = QPushButton('Open Communauto')
        self.openCommunautoButton.clicked.connect(self.on_openCommunautoButton_clicked)

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.on_search_button_clicked)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.on_refresh_button_clicked)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.on_stop_button_clicked)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.on_clear_button_clicked)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.close)

        self.updated_label = QLabel('Data Updated:')
        self.updated_value = QLabel('')

        self.vehicle_count_label = QLabel('Vehicle Count:')
        self.vehicle_count_value = QLabel('')

        self.vehicle_list = FilterWidget()
        self.vehicle_list.list_widget.itemClicked.connect(self.on_vehicle_list_item_clicked)

        self.show_map_button = QPushButton('Show Map')
        self.show_map_button.setEnabled(False)
        self.show_map_button.clicked.connect(self.on_show_map_button_clicked)

        self.radio_map = QLabel('Map')
        self.radio_details = QLabel('Vehicle Details')

        self.vehicle_map_label = QLabel()
        self.vehicle_map_label.setAlignment(Qt.AlignCenter)

        self.vehicle_details_text = QTextEdit()
        self.vehicle_details_text.setReadOnly(True)

        central_widget = QWidget()
        # super().setCentralWidget(central_widget)

        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(QLabel('Choose the distance:'))
        left_layout.addWidget(self.distance_slider)
        left_layout.addWidget(self.distance_label)
        left_layout.addWidget(QLabel('Enter sleep time (in seconds):'))
        left_layout.addWidget(self.sleep_time_input)
        left_layout.addWidget(QLabel('Enter longitude:'))
        left_layout.addWidget(self.longitude_input)
        left_layout.addWidget(QLabel('Enter latitude:'))
        left_layout.addWidget(self.latitude_input)
        left_layout.addWidget(self.openCommunautoButton)
        left_layout.addWidget(self.search_button)
        left_layout.addWidget(self.refresh_button)
        left_layout.addWidget(self.stop_button)
        left_layout.addWidget(self.clear_button)
        left_layout.addWidget(self.exit_button)

        right_layout.addWidget(self.updated_label)
        right_layout.addWidget(self.updated_value)
        right_layout.addWidget(self.vehicle_count_label)
        right_layout.addWidget(self.vehicle_count_value)
        right_layout.addWidget(self.vehicle_list)
        right_layout.addWidget(self.show_map_button)
        right_layout.addWidget(self.radio_map)
        right_layout.addWidget(self.vehicle_map_label)
        right_layout.addWidget(self.radio_details)
        right_layout.addWidget(self.vehicle_details_text)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)
    def on_search_button_clicked(self):
        distance = self.distance_slider.value()
        latitude = float(self.latitude_input.text())
        longitude = float(self.longitude_input.text())
        self.search_button.setEnabled(False)
        interval = int(self.sleep_time_input.text())
        self.toggle_auto_refresh(interval, distance, latitude, longitude)

    def on_refresh_button_clicked(self):
        distance = self.distance_slider.value()
        latitude = float(self.latitude_input.text())
        longitude = float(self.longitude_input.text())
        self.refresh(distance, latitude, longitude)

    def on_stop_button_clicked(self):
        self.search_button.setEnabled(True)
        self.show_map_button.setEnabled(False)
        self.stop_search()

    def on_clear_button_clicked(self):
        self.vehicle_list.clear()
        self.vehicle_details_text.clear()
        self.show_map_button.setEnabled(False)
        self.vehicle_map_label.clear()

    def on_show_map_button_clicked(self):
        vehicle_id = self.vehicle_list.currentItem().text()
        if vehicle_id.isdigit():
            vehicle_id = int(vehicle_id)
            self.show_map(vehicle_id)

    def on_vehicle_list_item_clicked(self, item):
        vehicle_id = item.text().split('\n')[0].split(' ')[1]
        if vehicle_id.isdigit():
            vehicle_id = int(vehicle_id)
            self.update_vehicle_details(str(self.get_vehicle_details(vehicle_id)))

    def update_vehicle_count(self, count):
        self.vehicle_count_value.setText(str(count))

    def update_vehicle_list(self, vehicles):
        self.vehicle_list.clear()
        for vehicle in vehicles:
            self.vehicle_list.add_item(vehicle)

    def update_time(self, time):
        self.updated_value.setText(time)

    def update_vehicle_map(self, image_path):
        pixmap = QPixmap(image_path)
        self.vehicle_map_label.setPixmap(pixmap)

    def update_vehicle_details(self, details):
        self.vehicle_details_text.setText(details)

    def show_location_on_map(self, lat, lon):
        self.latitude_input.setText(str(lat))
        self.longitude_input.setText(str(lon))

    def on_distance_slider_changed(self):
        distance = self.distance_slider.value()
        self.distance_label.setText(f"Distance: {distance} meters")

    def on_stop_button_clicked(self):
        self.search_button.setEnabled(True)
        self.show_map_button.setEnabled(False)
        self.stop_search()

    def refresh(self, distance, latitude, longitude):
        self.model.all_vehicle_group = self.find_all_vehicles(latitude, longitude)
        self.model.vehicle_group_within_radius = self.find_vehicles_within_radius(distance)
        self.update_list()
        self.update_vehicle_count(self.model.vehicle_count)
        self.update_time(time.strftime("%H:%M:%S", time.localtime()))

    def stop_search(self):
        self.stop_flag = True
        if self.refresh_thread:
            self.refresh_thread.stop()
            self.refresh_thread.join()
            self.refresh_thread = None

    def toggle_auto_refresh(self, interval, distance, latitude, longitude):
        if self.refresh_thread:
            self.refresh_thread.stop()
            self.refresh_thread = None
        else:
            self.stop_flag = False
            self.refresh_thread = RepeatTimer(interval, self.refresh, args=(distance, latitude, longitude))
            self.refresh_thread.start()

    def get_vehicle_details(self, vehicle_id):
        return fetch_vehicle_details(vehicle_id)

    def find_all_vehicles(self, lat, lng):
        self.vehicle_group = fetch_all_vehicles(lat, lng)
        self.vehicle_count = len(self.vehicle_group)
        return self.vehicle_group
    
    def find_vehicles_within_radius(self, distance):
        self.vehicle_group = self.vehicle_group.get_vehicle_within_radius(distance)
        return self.vehicle_group
    
    def update_list(self):
        vehicle_info_list = []
        for vehicle in self.model.vehicle_group_within_radius:
            vehicle_info = f"ID: {vehicle.vehicle_id}\nDistance: {vehicle.distance:.2f} meters"
            vehicle_info_list.append(vehicle_info)
        self.update_vehicle_list(vehicle_info_list)

    def on_openCommunautoButton_clicked(self):
        openURL("https://montreal.communauto.com/?city=montreal")

    

class View(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setWindowTitle('Communauto Watcher')

        self.tab_widget = QTabWidget()

        self.tab1 = CustomWidget(model)
        self.tab2 = QWidget()

        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")

        self.setCentralWidget(self.tab_widget)

