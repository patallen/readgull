import copy

from slugify import slugify

from readgull.settings import DEFAULT_CONFIG


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

        self.local_settings = {}
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

    def _set_meta_attrs(self):
        """
        This method takes care of converting the metadata provided to
        attributes of the instance that can be accessed using dot notation.
        """
        if self.local_metadata:
            for key, value in self.local_metadata.iteritems():
                setattr(self, key.lower(), value)

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

    def _check_required_attrs(self, metadata):
        """
        Checks that all of the required_meta fields specified in the
        local_settings are attributes of this class.
        """
        for attr in self.required_fields:
            if attr not in metadata.keys():
                raise ValueError('Check required fields for content type.')
