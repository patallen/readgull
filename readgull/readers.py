from markdown import Markdown


class BaseReader(object):

    file_extensions = ['md', 'markdown']

    def __init__(self, settings):
        self.settings = settings

    def read(self, path):
        """Read from file and return it's Markdown and metadata"""

        self._source_path = path
        self._markdown = Markdown(extensions=['meta'])
        with open(path) as text:
            markdown = self._markdown.convert(text.read())
            metadata = self._markdown.Meta
        return markdown, metadata
