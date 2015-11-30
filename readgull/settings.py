import inspect
import copy
import os

try:
    from importlib.machinery import SourceFileLoader

    def load_source(name, path):
        return SourceFileLoader(name, path).load_module()
except ImportError:
    import imp
    load_source = imp.load_source

DEFAULT_CONFIG = {
    'CONTENT_TYPES': {
        'article': {
            'required_meta': ['title'],
            'template': 'article.html'
        },
    },
    'PATH': os.curdir,
    'OUTPUT_PATH': 'output',
    'SITENAME': 'A ReadGull Site',
    'SITEURL': '',
    'EXCLUDE_PATHS': [''],
    'DEFAULT_AUTHOR': 'Admin',
    'MAX_EXCERPT_LENGTH': 255,
    'SLUG_SOURCE': 'title',
    'DEFAULT_CONTENT_TEMPLATE': 'content.html'
}


def get_settings_from_file(path):
    """Returns a dict of settings from a file"""
    module = load_source(path, os.path.basename(path))
    return get_settings_from_module(module)


def get_settings_from_module(module, default_config=DEFAULT_CONFIG):
    context = copy.deepcopy(default_config)
    if module is not None:
        context.update(
            (k, v) for k, v in inspect.getmembers(module) if k.isupper()
        )
    return context


def read_settings(path=None):
    # Make all paths absolute paths
    # Set BASE_PATH to dir where readgullconf.py is located
    # Set all other paths relative to BASE_PATH
    settings = get_settings_from_file(path)
    settings['BASE_PATH'] = base_path = os.path.dirname(path)

    for checkpath in ['PATH', 'OUTPUT_PATH']:
        if settings[checkpath] and not os.path.isabs(settings[checkpath]):
            settings[checkpath] = os.path.join(base_path, settings[checkpath])

    return settings
