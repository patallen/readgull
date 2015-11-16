from settings import get_settings_from_file
from readers import BaseReader
import time


class ReadGull(object):
    def __init__(self, settings):
        self.settings = settings
        self.output_path = settings['OUTPUT_PATH']
        self.path = settings['PATH']

    def print_settings(self):
        for setting in self.settings:
            print("{}: {}".format(setting, self.settings[setting]))

    def run(self):
        start_time = time.time()
        context = self.settings.copy()


def main():
    settings = {
        "OUTPUT_PATH": "output",
        "PATH": "content",
        "EXCLUDE_DIRS": ['poetry', 'songs']
    }

    r = ReadGull(settings)
    r.print_settings()
    reader = BaseReader(get_settings_from_file('readconfig.py'))
    reader.read('/Users/patallen/Code/Python/readgulldev/site/content/test.md')
