import os
import readgull


class Writer(object):

    def __init__(self, settings=None):
        if not settings:
            self.settings = readgull.settings.DEFAULT_CONFIG
        else:
            self.settings = settings

    def save(self, html, output_path, filename):
        save_path = os.path.join(output_path, filename)
        with open(save_path, 'w') as f:
            f.write(html)
