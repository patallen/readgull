from datetime import datetime
import os

from generators import ContextGenerator, ContentProcessor
from settings import read_settings
from utils.time import format_timedelta


class ReadGull(object):
    """
    Main Readgull class that handles the setup and running of all
    processes to complete the building of the static site.
    """
    def __init__(self, settings):
        self.settings = settings
        self.output_path = settings['OUTPUT_PATH']
        self.path = settings['PATH']
        self.content_types = settings['CONTENT_TYPES']

    def print_settings(self):
        """
        Temporary helper function to print the settings.
        """
        for setting in self.settings:
            print("{}: {}".format(setting, self.settings[setting]))

    def run(self):
        """This will run the generators"""
        context = {}
        start_time = datetime.now()
        for content_type in self.content_types:
            generator = ContextGenerator(self.settings, content_type)
            content = generator.get_content()
            if content:
                print(generator.content_group)
                context[generator.content_group] = content
        cp = ContentProcessor(context, settings=self.settings)
        cp.run()
        print("Time to complete: {}"
              .format(format_timedelta(datetime.now() - start_time)))


def main():
    readgull = ReadGull(read_settings(os.path.abspath('readconfig.py')))
    readgull.run()
