import os
import pprint

from datetime import datetime
from generators import Generator
from settings import read_settings


class ReadGull(object):
    """
    BASE_PATH : Path where readgullconf.py is located
    PATH : Path where content can be found
    OUTPUT_PATH : Path to dir where output will be placed
    """
    def __init__(self, settings):
        self.settings = settings
        self.output_path = settings['OUTPUT_PATH']
        self.path = settings['PATH']
        self.content_types = settings['CONTENT_TYPES']

    def print_settings(self):
        for setting in self.settings:
            print("{}: {}".format(setting, self.settings[setting]))

    def run(self):
        """This will run the generators"""
        context = {}
        start_time = datetime.now()
        for content_type in self.content_types:
            generator = Generator(self.settings, content_type)
            context[content_type] = generator.get_content()
        pprint.pprint(context)
        print("Time to complete: {}".format(datetime.now() - start_time))


def test_reader():
    readgull = ReadGull(read_settings(os.path.abspath('readconfig.py')))
    readgull.run()


def main():
    test_reader()
