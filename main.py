import PySimpleGUI as sg
import time
from logic import fetch_all_vehicles
from repeatTimer import RepeatTimer
import folium

# Define the GUI layout
layout = [
    [
        sg.Column([
            [sg.Text('Enter distance (in meters): '), sg.Input(key='distance')],
            [sg.Text('Enter sleep time (in seconds): '), sg.Input(key='sleep_time')],
            [sg.Text('Enter longitude: '), sg.Input(key='longitude')],
            [sg.Text('Enter latitude: '), sg.Input(key='latitude')],
            [sg.Button('Search'), sg.Button('Stop'), sg.Button('Clear'), sg.Button('Exit')],
            [sg.Text('Data Updated:'), sg.Text(time.strftime('%Y-%m-%d %H:%M:%S'), size=(20, 1), key='updated')],
            [sg.Text('Vehicle Count:'), sg.Text('', size=(20, 1), key='vehicle_count')],
            [sg.Frame('Vehicle List', [[sg.Listbox(values=[], size=(40, 20), key='vehicle_list')]])],
        ], element_justification='left', expand_x=True, expand_y=True),
        sg.Column([
            [
                sg.Radio('Map', 'radio', key='radio_map', default=True),
                sg.Radio('Vehicle Details', 'radio', key='radio_details')
            ],
            [
                sg.Column([
                    [sg.Image(key='vehicle_map', visible=True)]
                ], key='column_map', visible=True, element_justification='center'),
                sg.Column([
                    [sg.Multiline(size=(80, 20), key='vehicle_details', visible=False)]
                ], key='column_details', visible=False, element_justification='center')
            ]
        ], element_justification='center', expand_x=True, expand_y=True)
    ]
]


class Model:
    def __init__(self, view):
        self.view = view
        self.vehicle_group = None
        self.vehicle_count = 0
        self.time = time.strftime('%Y-%m-%d %H:%M:%S')

    def update_vehicle_count(self, count):
        self.vehicle_count = count
        self.view.update_vehicle_count(count)

    def update_time(self, time):
        self.time = time
        self.view.update_data_updated(time)

    def update_list(self, vehicles):
        self.vehicle_group = vehicles
        result = []
        for e in vehicles:
            result.append(f"Vehicle ID: {e.vehicle_id}, Distance: {int(e.distance)} meters\n")
        self.view.update_vehicle_list(result)
    
    def update_map(self, image_path):
        self.vehicle_group = image_path

    def generate_map(self, lat, lon):
        # Create a folium map centered around the given GPS coordinates
        map_obj = folium.Map(location=[lat, lon], zoom_start=15)

        # Add a marker at the specified location
        folium.Marker([lat, lon]).add_to(map_obj)

        # Save the map as an HTML file
        map_obj.save('map.html')

        # Update the view with the map file path
        self.view.update_vehicle_map('map.html')



class View:
    def __init__(self):
        self.window = sg.Window('Communauto Watcher', layout, finalize=True)

    def read_input(self):
        event, values = self.window.read()
        return event, values

    def close(self):
        self.window.close()

    def update_data_updated(self, text):
        self.window['updated'].update(text)

    def update_vehicle_count(self, count):
        self.window['vehicle_count'].update(f"Found {count} vehicles")

    def update_vehicle_list(self, vehicles):
        self.window['vehicle_list'].update(values=vehicles)

    def update_vehicle_map(self, image_path):
        self.window['vehicle_map'].update(filename=image_path)

    def update_vehicle_details(self, details):
        self.window['vehicle_details'].update(value=details)

    def clear(self):
        self.window['vehicle_list'].update(values=[])
        self.window['vehicle_map'].update(filename='')
        self.window['vehicle_details'].update(value='')
        self.window['vehicle_count'].update(value='')
        self.window['updated'].update(value='')

    def update_vehicle_map(self, map_path):
        self.window['vehicle_map'].update(filename=map_path)

    def error(self, message):
        sg.popup_error(message)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.refresh_enabled = False
        self.refresh_thread = None  # Initialize the refresh_thread variable

    def toggle_refresh(self, enabled):
        self.refresh_enabled = enabled  # Set the refresh state based on the enabled parameter

    def find_vehicles(self, distance, latitude, longitude):
        # Update the model and trigger the necessary computations
        self.model.vehicle_group = fetch_all_vehicles(latitude, longitude)

        # Update the view based on the model
        self.model.update_time(time.strftime('%Y-%m-%d %H:%M:%S'))
        self.model.update_vehicle_count(len(self.model.vehicle_group.vehicles))
        self.model.update_list(self.model.vehicle_group.get_vehicle_within_radius(distance).vehicles)

    def error(self, message):
        self.view.error(message)

    def clear(self):
        self.view.clear()

    def run(self):
        while True:
            try:
                event, values = self.view.read_input()
                if event == sg.WINDOW_CLOSED or event == 'Exit':
                    self.toggle_refresh(False)
                    break
                elif event == 'Search' and not self.refresh_enabled:
                    # Start the refresh thread
                    self.toggle_refresh(True)  # Enable refresh
                    distance = int(values['distance'])
                    latitude = float(values['latitude'])
                    longitude = float(values['longitude'])
                    self.find_vehicles(distance, latitude, longitude)
                    self.refresh_thread = RepeatTimer(int(values['sleep_time']), self.find_vehicles, args=(distance, latitude, longitude))
                    self.refresh_thread.start()
                elif event == 'Stop':
                    self.toggle_refresh(False)
                    if self.refresh_thread:
                        self.refresh_thread.cancel()
                elif event == 'Clear':
                    self.clear()
                else:
                    raise ValueError("Unknown event in the main loop")
            except Exception as e:
                self.error(e)



# Create an instance of the view
view = View()

# Create an instance of the model
model = Model(view)

# Create an instance of the controller and pass the model and view
controller = Controller(model, view)

# Run the application
controller.run()

# Close the GUI
view.close()
