import copy

from readgull.settings import DEFAULT_CONFIG


class Content(object):
    """
    This object will contain the information, properties, and functions for
    each piece of content for all content_types. Information in instances
    of this class will be accessible through dot notation.
    """

    def __init__(self, content_name, content, metadata, settings=None):
        self.content_name = content_name
        self.content = content
        self.local_metadata = metadata
        self._set_meta_attrs()

        if settings is None:
            settings = copy.deepcopy(DEFAULT_CONFIG)

        self.settings = settings
        self.local_settings = {}
        if self.settings.get(self.content_name) is not None:
            self.local_settings = self.settings[self.content_name]

    def _set_meta_attrs(self):
        """
        This method takes care of converting the metadata provided to
        attributes of the instance that can be accessed using dot notation.
        """

        if self.local_metadata:
            for key, value in self.local_metadata.iteritems():
                setattr(self, key.lower(), value)
