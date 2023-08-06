"""
Summary.

    Core Logic Module -- Common Functionality

"""
import os
import sys
import re
import inspect
import logging
from shutil import which
from xlines.colors import Colors
from xlines.statics import local_config
from xlines._version import __version__
from xlines.variables import *

logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)

try:
    from xlines.oscodes_unix import exit_codes
    os_type = 'Linux'
    user_home = os.getenv('HOME')
    splitchar = '/'                             # character for splitting paths (linux)
    acct = Colors.ORANGE
    text = Colors.BRIGHT_PURPLE
    TITLE = Colors.WHITE + Colors.BOLD
except Exception:
    from xlines.oscodes_win import exit_codes    # non-specific os-safe codes
    os_type = 'Windows'
    user_home = os.getenv('username')
    splitchar = '\\'                            # character for splitting paths (windows)
    acct = Colors.CYAN
    text = Colors.LT2GRAY
    TITLE = Colors.WHITE + Colors.BOLD


def absolute_paths(path_list):
    """
        Determines if filesystem paths are absolute or relative

    Args:
        :path_list (list):
            [
                '/usr/local/bin/python3',
                '/home/user/myfile.txt',
                '../myfile.txt'
            ]

    Returns:
        True (absolute paths) || False (relative  paths), TYPE: bool

    """
    prefix = '/'
    if any(i.startswith(prefix) for i in path_list):
        return True
    return False


def is_binary_external(filepath):
    try:
        f = open(filepath, 'rb').read(1024)
        textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        fx = lambda bytes: bool(bytes.translate(None, textchars))
    except Exception:
        return True
    return fx(f)


def linecount(path, whitespace=True):
    if whitespace:
        return len(open(path).readlines())
    return len(list(filter(lambda x: x != '\n', open(path).readlines())))


def remove_duplicates(duplicates):
    """
    Summary.

        Module function utilsing a generator to remove duplicates
        from large scale lists with minimal resource use

    Args:
        duplicates (list): contains repeated elements

    Returns:
        list object (iter)
    """
    uniq = []

    def dedup(d):
        for element in d:
            if element not in uniq:
                uniq.append(element)
                yield element
    return [x for x in dedup(duplicates)]


def remove_illegal(d, illegal):
    """
        Removes excluded file types

    Args:
        :d (list): list of filesystem paths ending with a file object
        :illegal (list):  list of file type extensions for to be excluded

    Returns:
        legal filesystem paths (str)
    """
    def parse_list(path):
        """Reads in list from file object"""
        with open(path) as f1:
            return [x.strip() for x in f1.readlines()]

    def is_binary(filepath):
        try:
            f = open(filepath, 'rb').read(1024)
            textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
            fx = lambda bytes: bool(bytes.translate(None, textchars))
            return fx(f)
        except Exception:
            return True

    bad = []

    try:
        illegal_dirs = parse_list(local_config['EXCLUSIONS']['EX_DIR_PATH'])
    except KeyError:
        illegal_dirs = ['pycache', 'venv']

    # filter for illegal or binary file object
    for fpath in d:

        fobject = os.path.split(fpath)[1]

        # filter for illegal dirs first, then files, then binary
        if list(filter(lambda x: x in fpath, illegal_dirs)):
            bad.append(fpath)

        elif ('.' in fobject) and ('.' + fobject.split('.')[1] in illegal):
            bad.append(fpath)

        if is_binary(fpath):
            bad.append(fpath)

    return sorted(list(set(d) - set(bad)))


def locate_fileobjects(origin, abspath=True):
    """
    Summary.

        - Walks local fs directories identifying all git repositories

    Args:
        - origin (str): filesystem directory location
        - abspath (bool): return absolute paths relative to current cursor position

    Returns:
        - paths, TYPE: list
        - Format:

         .. code-block:: json

                [
                    '/cloud-custodian/tools/c7n_mailer/c7n_mailer/utils_email.py',
                    '/cloud-custodian/tools/c7n_mailer/c7n_mailer/slack_delivery.py',
                    '/cloud-custodian/tools/c7n_mailer/c7n_mailer/datadog_delivery.py',
                    '/cloud-custodian/tools/c7n_sentry/setup.py',
                    '/cloud-custodian/tools/c7n_sentry/test_sentry.py',
                    '/cloud-custodian/tools/c7n_kube/setup.py',
                    '...
                ]

    """
    def relpath_normalize(path):
        """
        Prepends correct relative filesystem syntax if analyzed pwd
        """
        if pattern_hidden.match(path) or pattern_asci.match(path):
            return './' + path
        elif path.startswith('..'):
            return path

    pattern_hidden = re.compile('^.[a-z]+')                    # hidden file (.xyz)
    pattern_asci = re.compile('^[a-z]+', re.IGNORECASE)        # standalone, regular file
    fobjects = []

    if os.path.isfile(origin):
        return [origin]

    for root, dirs, files in os.walk(origin):
        for file in [f for f in files if '.git' not in root]:
            try:

                if abspath:
                    # absolute paths (default)
                    _path = os.path.abspath(os.path.join(root, file))
                else:
                    # relative paths (optional)
                    _path = os.path.relpath(os.path.join(root, file))
                    _path = relpath_normalize(_path)

                fobjects.append(_path)

            except OSError:
                logger.exception(
                    '%s: Read error while examining local filesystem path (%s)' %
                    (inspect.stack()[0][3], _path)
                )
                continue
    return remove_duplicates(fobjects)


def print_header(w):
    total_width = w + local_config['OUTPUT']['COUNT_COLUMN_WIDTH'] + 1
    header_lhs = 'object'
    header_rhs = 'line count'
    tab = '\t'.expandtabs(total_width - len(header_lhs) - len(header_rhs))
    tab4 = '\t'.expandtabs(4)
    print(tab4 + (horiz * (total_width)))
    print(f'{tab4}{header_lhs}{tab}{header_rhs}')
    print(tab4 + (horiz * (total_width)))


def print_footer(total, object_count, w):
    """
    Print total number of objects and cumulative total line count
    """
    total_width = w + local_config['OUTPUT']['COUNT_COLUMN_WIDTH'] + 1

    # add commas
    total_lines = '{:,}'.format(object_count)

    # calc dimensions; no color codes
    msg = 'Total ({} objects):'.format(total_lines)
    tab = '\t'.expandtabs(total_width - len(msg) - len(str(total)) - 1)

    # redefine with color codes added
    msg = f'Total ({title + "{:,}".format(object_count) + rst} objects):'
    tab4 = '\t'.expandtabs(4)

    # divider pattern
    print(tab4 + (horiz * (total_width)))

    # ending summary stats line
    print(f'{tab4}{msg}{tab}{highlight + "{:,}".format(total) + rst:>10}' + '\n')
