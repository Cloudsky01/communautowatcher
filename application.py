import PySimpleGUI as sg
import time
from logic import main


layout = [
    [
        sg.Column([
            [sg.Text('Enter distance (in meters): '), sg.Input(key='distance')],
            [sg.Text('Enter sleep time (in seconds): '), sg.Input(key='sleep_time')],
            [sg.Button('Search'), sg.Button('Stop'), sg.Button('Clear'), sg.Button('Exit')],
            [sg.Text('Data Updated:'), sg.Text(time.strftime('%Y-%m-%d %H:%M:%S'), size=(20, 1), key='updated')],
            [sg.Text('Vehicle Count:'), sg.Text('', size=(20, 1), key='vehicle_count')],
            [sg.Frame('Vehicle List', [[sg.Listbox(values=[], size=(40, 20), key='vehicle_list')]])],
        ], element_justification='center', expand_x=True, expand_y=True),
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


class Application():
    def __init__(self):
        self.window = sg.Window('Communauto Watcher', layout)
    
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

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            elif event == 'Search':
                self.find_distance(values['distance'])
            elif event == 'Stop':
                self.stop()
            elif event == 'Clear':
                self.clear()
            elif event == 'radio_map':
                self.window['column_map'].update(visible=True)
                self.window['column_details'].update(visible=False)
            elif event == 'radio_details':
                self.window['column_map'].update(visible=False)
                self.window['column_details'].update(visible=True)
        self.window.close()
