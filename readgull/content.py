class Content(object):
    """
    This object will contain the information, properties, and functions for
    each piece of content for all content_types. Information in instances
    of this class will be accessible through dot notation.
    """

    def __init__(self, content, metadata):
        self.content = content
        self.local_metadata = metadata
        self._set_meta_attrs()

    def _set_meta_attrs(self):
        """
        This method takes care of converting the metadata provided to
        attributes of the instance that can be accessed using dot notation.
        """
        if self.local_metadata:
            for key, value in self.local_metadata.iteritems():
                setattr(self, key.lower(), value)
