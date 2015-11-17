from settings import read_settings
import os
from generators import Generator


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

    def print_settings(self):
        for setting in self.settings:
            print("{}: {}".format(setting, self.settings[setting]))

    def run(self):
        """This will run the generators"""
        # start_time = time.time()
        # context = self.settings.copy()


def main():
    r = ReadGull(read_settings(os.path.abspath('readconfig.py')))
    # r.print_settings()
    gen = Generator(r.settings, 'article')
    print gen.filepaths
