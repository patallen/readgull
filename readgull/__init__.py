from settings import get_settings_from_file, parse_settings
from readers import BaseReader
from generators import Generator
import time
import os


class ReadGull(object):
    def __init__(self, settings):
        self.settings = settings
        self.output_path = settings['OUTPUT_PATH']
        self.path = settings['PATH']

    def print_settings(self):
        for setting in self.settings:
            print("{}: {}".format(setting, self.settings[setting]))

    def run(self):
        """This will run the generators"""
        start_time = time.time()
        context = self.settings.copy()


def main():
    settings = get_settings_from_file('readconfig.py')
    r = ReadGull(settings)
    r.print_settings()
