# this is the json file handler for the project
import json


class JSONHandler:

    def __init__(self):

        self.json_object = None
        self.file_name = None

    def load_file(self, file):
        with open(file, 'r') as f:
            self.json_object = json.load(f)
        self.file_name = file

    def close(self):
        self.file_name = None

    def get_data(self):
        return self.json_object

    def save(self, json_data):
        with open(self.file_name, 'w') as f:
            json.dump(json_data, f, indent=4)
