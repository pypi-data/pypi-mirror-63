# -*- coding: utf-8 -*-
"""
The :mod:`neurotic.scripts` module handles starting the app from the command
line. It also provides a convenience function for quickly launching the app
using minimal metadata or an existing Neo :class:`Block <neo.core.Block>`, and
another for starting a Jupyter server with an example notebook.

.. autofunction:: quick_launch

.. autofunction:: launch_example_notebook
"""

import sys
import argparse
import subprocess
import pkg_resources

from ephyviewer import QT, mkQApp

from . import __version__
from .datasets.data import load_dataset
from .gui.config import EphyviewerConfigurator, available_themes, available_ui_scales
from .gui.standalone import MainWindow

import logging
logger = logging.getLogger(__name__)


def parse_args(argv):
    """

    """

    description = """
    neurotic lets you curate, visualize, annotate, and share your behavioral
    ephys data.
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('file', nargs='?', default=None,
                        help='the path to a metadata YAML file (default: an ' \
                             'example file)')
    parser.add_argument('dataset', nargs='?', default=None,
                        help='the name of a dataset in the metadata file to ' \
                             'select initially (default: the first entry in ' \
                             'the metadata file)')

    parser.add_argument('-V', '--version', action='version',
                        version='neurotic {}'.format(__version__))
    parser.add_argument('--debug', action='store_true', dest='debug',
                        help='enable detailed log messages for debugging')
    parser.add_argument('--no-lazy', action='store_false', dest='lazy',
                        help='do not use fast loading (default: use fast ' \
                             'loading)')
    parser.add_argument('--thick-traces', action='store_true', dest='thick',
                        help='enable support for traces with thick lines, ' \
                             'which has a performance cost (default: ' \
                             'disable thick line support)')
    parser.add_argument('--show-datetime', action='store_true', dest='datetime',
                        help='display the real-world date and time, which ' \
                             'may be inaccurate depending on file type and ' \
                             'acquisition software (default: do not display)')
    parser.add_argument('--ui-scale', dest='ui_scale',
                        choices=available_ui_scales, default='medium',
                        help='the scale of user interface elements, such as ' \
                             'text (default: medium)')
    parser.add_argument('--theme', choices=available_themes, default='light',
                        help='a color theme for the GUI (default: light)')

    parser.add_argument('--launch-example-notebook', action='store_true',
                        help='launch Jupyter with an example notebook ' \
                             'instead of starting the standalone app (other ' \
                             'args will be ignored)')

    args = parser.parse_args(argv[1:])

    if args.debug:
        logger.parent.setLevel(logging.DEBUG)

        # lower the threshold for PyAV messages printed to the console from
        # critical to warning
        logging.getLogger('libav').setLevel(logging.WARNING)

        if not args.launch_example_notebook:
            # show only if Jupyter won't be launched, since the setting will
            # not carry over into the kernel started by Jupyter
            logger.debug('Debug messages enabled')

    return args

def win_from_args(args):
    """

    """

    win = MainWindow(file=args.file, initial_selection=args.dataset,
                     lazy=args.lazy, theme=args.theme, ui_scale=args.ui_scale,
                     support_increased_line_width=args.thick,
                     show_datetime=args.datetime)
    return win

def launch_example_notebook():
    """
    Start a Jupyter server and open the example notebook.
    """

    path = pkg_resources.resource_filename('neurotic',
                                           'example/example-notebook.ipynb')
    out = None

    # check whether Jupyter is installed
    try:
        out = subprocess.Popen(['jupyter', 'notebook', '--version'],
                               stdout=subprocess.PIPE).communicate()[0]
    except FileNotFoundError as e:
        logger.error('Unable to verify Jupyter is installed using "jupyter '
                     'notebook --version". Is it installed?')

    if out:
        # run Jupyter on the example notebook
        try:
            out = subprocess.Popen(['jupyter', 'notebook', path],
                                   stdout=subprocess.PIPE).communicate()[0]
        except FileNotFoundError as e:
            logger.error(f'Unable to locate the example notebook at {path}')

def main():
    """

    """

    args = parse_args(sys.argv)
    if args.launch_example_notebook:
        launch_example_notebook()
    else:
        logger.info('Loading user interface')
        app = mkQApp()
        splash = QT.QSplashScreen(QT.QPixmap(':/neurotic-logo-300.png'))
        splash.show()
        win = win_from_args(args)
        win.show()
        splash.finish(win)
        logger.info('Ready')
        app.exec_()

def quick_launch(metadata={}, blk=None, lazy=True):
    """
    Load data, configure the GUI, and launch the app with one convenient
    function.

    This function allows **neurotic** to be used easily in interactive sessions
    and scripts. For example, dictionaries can be passed as metadata:

    >>> metadata = {'data_file': 'data.axgx'}
    >>> neurotic.quick_launch(metadata=metadata)

    An existing Neo :class:`Block <neo.core.Block>` can be passed directly:

    >>> neurotic.quick_launch(blk=my_neo_block)

    This function is equivalent to the following:

    >>> blk = load_dataset(metadata, blk, lazy=lazy)
    >>> ephyviewer_config = EphyviewerConfigurator(metadata, blk, lazy=lazy)
    >>> ephyviewer_config.show_all()
    >>> ephyviewer_config.launch_ephyviewer()
    """

    # make sure this matches the docstring after making changes
    blk = load_dataset(metadata, blk, lazy=lazy)
    ephyviewer_config = EphyviewerConfigurator(metadata, blk, lazy=lazy)
    ephyviewer_config.show_all()
    ephyviewer_config.launch_ephyviewer()
