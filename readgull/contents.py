import copy
import os
import readgull

from slugify import slugify

from readgull.settings import DEFAULT_CONFIG


class ContentType(object):
    """
    Object will contain all the information for a content type and
    the contents under it will be iterable.
    """
    def __init__(self, content_type, settings=None):
        if settings is None:
            settings = DEFAULT_CONFIG
        self.settings = settings
        self.type_settings = settings['CONTENT_TYPES'].get(content_type)
        self.name = content_type
        self.content = []

        file_extension = self.type_settings.get('output_extension')
        if file_extension is None:
            file_extension = settings['DEFAULT_OUTPUT_EXTENSION']
        self.file_extension = file_extension or 'html'

    def __iter__(self):
        return self.content.__iter__()

    @property
    def pluralized(self):
        return "{}s".format(self.name)

    @property
    def base_output_path(self):
        path_string = self.type_settings['output_path'] or self.pluralized
        return os.path.join(
            os.path.abspath(self.settings['PATH']),
            self.settings['OUTPUT_PATH'],
            path_string
        )

    def add_contents(self, contents):
        """
        Add an instance of Content or a list of instances of Content
        to the iterable of this class.
        """
        if isinstance(contents, (list, tuple)):
            for c in contents:
                self.add_content(c)
        elif isinstance(contents, Content):
            self.add_content(contents)
        else:
            raise TypeError

    def add_content(self, content):
        if type(content) is Content:
            self.content.append(content)
        else:
            print content
            raise TypeError

    def get_content_path(self, content):
        """
        Given a piece of content, return the content's absolute
        output path relative to the ContentType's base_path.
        """
        if isinstance(content, Content):
            return os.path.join(
                self.base_output_path,
                "{}.{}".format(content.slug, self.file_extension)
            )
        else:
            raise TypeError


class Content(object):
    """
    This object will contain the information, properties, and functions for
    each piece of content for all content_types. Information in instances
    of this class will be accessible through dot notation.
    """

    def __init__(self, content_name, content, metadata, settings=None):

        self.content_name = content_name
        if settings is None:
            settings = copy.deepcopy(DEFAULT_CONFIG)
        self.settings = settings

        type_settings = self.settings.get('CONTENT_TYPES')
        self.local_settings = type_settings.get(self.content_name)
        self.required_fields = self.local_settings.get('required_meta')

        self.local_metadata = metadata
        self.content = content

        self._check_required_attrs(metadata)
        # Setters
        self._set_meta_attrs()
        self._set_excerpt(content)
        self._set_slug()
        self._set_content_url()

    def to_dict(self):
        """Returns the instances attributes as a dictionary."""
        rv = self.__dict__
        del rv['settings']
        return rv

    def _set_meta_attrs(self):
        """
        This method takes care of converting the metadata provided to
        attributes of the instance that can be accessed using dot notation.
        """
        if self.local_metadata:
            for key, value in self.local_metadata.iteritems():
                setattr(self, key.lower(), value)

        # Set the template based on what we have in the metadata,
        # then local settings, then default to settings
        if not hasattr(self, 'template'):
            if self.local_settings.get('template'):
                self.template = self.local_settings['template']
            else:
                self.template = self.settings['DEFAULT_CONTENT_TEMPLATE']

    def _set_excerpt(self, content, excerpt_length=None):
        """
        This method sets the excerpt equal to the beginning of the content
        up to the first X('MAX_EXCERPT_LENGTH') characters.
        """
        if excerpt_length is None:
            excerpt_length = self.settings['MAX_EXCERPT_LENGTH']
        excerpt = content[:excerpt_length]
        excerpt += '...'
        self.excerpt = excerpt

    def _set_slug(self):
        """
        Try to set the content's slug based on the attribute specified
        in the settings SLUG_SOURCE if no slug exists for the content.
        """
        if not hasattr(self, 'slug'):
            try:
                slug_source = getattr(self, self.settings['SLUG_SOURCE'])
                self.slug = slugify(slug_source)
            except:
                raise ValueError("Could not set a slug.")

    def _set_content_url(self):
        """Set the relative path to the content to be used as a link"""
        output_path = self.local_settings.get('output_path')
        if not output_path:
            output_path = '{}s'.format(self.content_name)
        self.content_url = '/{}/{}.html'.format(output_path, self.slug)

    def _check_required_attrs(self, metadata):
        """
        Checks that all of the required_meta fields specified in the
        local_settings are attributes of this class.
        """
        for attr in self.required_fields:
            if attr not in metadata.keys():
                raise ValueError('Check required fields for content type.')
