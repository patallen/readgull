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
        if self.settings.get(self.content_name) is not None:
            self.local_settings = self.settings[self.content_name]

        self.local_metadata = metadata
        self.content = content

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
        Try to set the content's slug based on it's title if no slug
        if no slug attribute exists for the content.
        """
        if not hasattr(self, 'slug'):
            if hasattr(self, 'title'):
                self.slug = slugify(self.title)
            else:
                raise Exception("Content must have a title or slug.")
