from datetime import datetime
import os
import shutil

from generators import ContextGenerator, ContentProcessor
from contents import ContentType
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

    def run(self):
        """
        This will run the generators, content processors, and use the
        writers write the necessary files to the output directory.
        """
        context = {}
        start_time = datetime.now()
        for content_type in self.content_types:
            generator = ContextGenerator(self.settings, content_type)
            content = generator.get_content()
            if content:
                ct = ContentType(content_type, self.settings)
                for c in content:
                    ct.add_content(c)
                context[generator.content_group] = ct

        # remove current output dir and create new
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)
        os.mkdir(self.output_path)

        cp = ContentProcessor(context, settings=self.settings)
        cp.run()
        print("Time to complete: {}"
              .format(format_timedelta(datetime.now() - start_time)))


def main():
    readgull = ReadGull(read_settings(os.path.abspath('readconfig.py')))
    readgull.run()
