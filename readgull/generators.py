import os
from readers import BaseReader
import slugify
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
        self.content_type = self._get_content_name(content_type)
        self.content_path = self._get_content_path(self.content_type)
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

    def _get_content_name(self, content_type):
        """Generates a name for the content type passed in"""
        return content_type.lower().strip()

    def _get_content_path(self, content_type):
        """Gets the content directory for the content_type"""
        return os.path.join(
            os.path.abspath(self.settings['PATH']),
            '{}s'.format(content_type))

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
            metadata[key] = value[0]
        return metadata

    def _create_slug(self, filepath):
        """
        Creates a slug by removing the file extension from the basepath
        and then slugifying the result with the slugify library.
        """
        base = os.path.basename(filepath)
        noext = os.path.splitext(base)[0]
        slug = slugify.slugify(noext)
        return slug
