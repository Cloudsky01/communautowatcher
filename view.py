from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QListWidget, QSlider, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from logic import fetch_all_vehicles

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Communauto Watcher')

        self.distance_label = QLabel()
        self.distance_slider = QSlider(Qt.Horizontal)
        self.distance_slider.setRange(1, 1000)
        self.distance_slider.setValue(100)
        self.distance_slider.valueChanged.connect(self.on_distance_slider_changed)

        self.refresh_interval_input = QLineEdit()

        self.sleep_time_input = QLineEdit()

        self.longitude_input = QLineEdit()

        self.latitude_input = QLineEdit()

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

        self.vehicle_list = QListWidget()
        self.vehicle_list.currentRowChanged.connect(self.on_vehicle_list_current_row_changed)

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
        self.setCentralWidget(central_widget)

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

        self.controller = None

    def on_search_button_clicked(self):
        distance = self.distance_slider.value()
        latitude = float(self.latitude_input.text())
        longitude = float(self.longitude_input.text())
        self.search_button.setEnabled(False)
        interval = int(self.sleep_time_input.text())
        self.controller.toggle_auto_refresh(interval, distance, latitude, longitude)

    def on_refresh_button_clicked(self):
        distance = self.distance_slider.value()
        latitude = float(self.latitude_input.text())
        longitude = float(self.longitude_input.text())
        self.controller.refresh(distance, latitude, longitude)

    def on_stop_button_clicked(self):
        self.search_button.setEnabled(True)
        self.show_map_button.setEnabled(False)
        self.controller.stop_search()

    def on_clear_button_clicked(self):
        self.vehicle_list.clear()
        self.vehicle_details_text.clear()
        self.show_map_button.setEnabled(False)
        self.vehicle_map_label.clear()

    def on_show_map_button_clicked(self):
        vehicle_id = self.vehicle_list.currentItem().text()
        if vehicle_id.isdigit():
            vehicle_id = int(vehicle_id)
            self.controller.show_map(vehicle_id)

    def on_vehicle_list_current_row_changed(self):
        vehicle_id = self.vehicle_list.currentItem().text()
        if vehicle_id.isdigit():
            vehicle_id = int(vehicle_id)
            # self.controller.show_details(vehicle_id)

    def update_vehicle_count(self, count):
        self.vehicle_count_value.setText(str(count))

    def update_vehicle_list(self, vehicles):
        self.vehicle_list.clear()
        self.vehicle_list.addItems(vehicles)

    def update_time(self, time):
        self.updated_value.setText(time)

    def update_vehicle_map(self, image_path):
        pixmap = QPixmap(image_path)
        self.vehicle_map_label.setPixmap(pixmap)

    def show_location_on_map(self, lat, lon):
        self.latitude_input.setText(str(lat))
        self.longitude_input.setText(str(lon))

    def on_distance_slider_changed(self):
        distance = self.distance_slider.value()
        self.distance_label.setText(f"Distance: {distance} meters")

    def on_stop_button_clicked(self):
        self.search_button.setEnabled(True)
        self.show_map_button.setEnabled(False)
        self.controller.stop_search()