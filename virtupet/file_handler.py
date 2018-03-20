# this is the json file handler for the project
import json


class JSONHandler:

    def __init__(self):

        self.json_object = None
        self.file_name = None

    def load_file(self, file):
        with open(file, 'r') as f:
            self.json_object = json.load(f)

    def get_data(self):
        return self.json_object
