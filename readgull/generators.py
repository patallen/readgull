import os
from readers import BaseReader
from jinja2 import Environment, FileSystemLoader
import pprint
from readgull.content import Content


class ContextGenerator(object):
    """
    ContextGenerator will be run for each content type. For each type the
    ContextGenerator will:
    1. Gather each filename/path of each piece of content.

    2. Each piece of content will be stored in an instance of Content,
    where the metadta and content will be converted to attributes.

    3. Take the content gathered and use Jinja2 to parse it into HTML to be
    written by the Writer class.
    """
    def __init__(self, settings, content_type):
        self.settings = settings
        self.content_type = content_type
        self.content_group = self._get_content_group(content_type)
        self.content_path = self._get_content_path(self.content_group)
        self.filepaths = self._get_filepaths()
        self.reader = BaseReader(settings)
        self.read_extensions = self.reader.file_extensions

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

    def _get_content_group(self, content_type):
        """Generates a name for the content type passed in"""
        return "{}s".format(content_type.lower().strip())

    def _get_content_path(self, content_group):
        """Gets the content directory for the content_type"""
        return os.path.join(
            os.path.abspath(self.settings['PATH']),
            content_group)

    def get_content(self):
        """
        Gets the content of all files in the directory(s) for the
        generator's given content type.
        """
        rv = []
        for file in self.filepaths:
            content, metadata = self.reader.read(file)
            metadata = self._parse_metadata(metadata)
            piece = Content(self.content_type, content, metadata)
            rv.append(piece)

        return rv

    def _parse_metadata(self, metadata):
        """
        Takes a metadata dict and removes it's values from the list that
        they are put into by markdown's meta extension.
        """
        for key, value in metadata.iteritems():
            val = value[0]
            if key in self.settings['ALLOWED_MULTIPLES']:
                if "," in val:
                    multilist = [v.strip() for v in val.split(',')]
                    metadata[key] = multilist
            else:
                metadata[key] = val
        return metadata


class ContentProcessor(object):
    """
    Takes the context generated by the ContextGenerators and creates the
    content using the templates provided.
    """

    def __init__(self, context, settings=None):
        self.context = context
        self.settings = settings
        self.theme_dir = settings.get('THEME_DIR')
        self.environment = self._set_environment(self.theme_dir)

    def _set_environment(self, theme_dir):
        loader = FileSystemLoader(theme_dir)
        env = Environment(loader=loader)
        return env

    def index(self):
        index = self.environment.get_template('index.html')
        print index.render(self.context)

    def run(self):
        pprint.pprint(self.context)
        self.index()
