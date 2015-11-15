from settings import get_settings_from_file


class ReadGull(object):
    def __init__(self, settings):
        self.settings = settings
        self.output_path = settings['OUTPUT_PATH']
        self.path = settings['PATH']

    def print_settings(self):
        for setting in self.settings:
            print("{}: {}".format(setting, self.settings[setting]))


if __name__ == '__main__':
    settings = {
        "OUTPUT_PATH": "output",
        "PATH": "content",
        "EXCLUDE_DIRS": ['poetry', 'songs']
    }

    r = ReadGull(settings)
    r.print_settings()
    print(get_settings_from_file('readconfig.py'))
