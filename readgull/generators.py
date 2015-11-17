import os
from readers import BaseReader


class Generator(object):
    """
    Generator will be run for each content type. For each content type, the
    Generator will:
    1. Gather each filename/path of each piece of content.

    Stored in context by the Generator
    context[contents] = {
        article1 : {
            title:,
            date_created:,
            author:,
            excerpt:,
            markdown:,
        },
        article2 : {
            title:,
            date_created:,
            author:,
            excerpt:,
            markdown:,
        }
    }
    """
    def __init__(self, settings, content_type):
        self.settings = settings
        self.content_type = self._get_content_name(content_type)
        self.content_path = self._get_content_path(self.content_type)
        self.filepaths = self._get_filepaths()
        self.reader = BaseReader(settings)

    def _get_filepaths(self):
        """
        Get the filepaths for each piece of conent for the given content type.
        """
        all_files = os.listdir(self.content_path)
        files = []
        for f in all_files:
            if f.endswith('.md'):
                files.append(os.path.join(self.content_path, f))

        return files

    def _get_content_name(self, content_type):
        """Generates a name for the content type passed in"""
        return content_type.lower().strip()

    def _get_content_path(self, content_type):
        """Gets the content directory for the content_type"""
        return os.path.join(
            os.path.abspath(self.settings['PATH']),
            '{}s'.format(content_type))

    def get_content(self):
        content = {}

        content[self.content_type + 's'] = {}

        for file in self.filepaths:
            # TODO: Somehow name the content appropriately
            content[self.content_type + 's'][file] = self.reader.read(file)

        return content


