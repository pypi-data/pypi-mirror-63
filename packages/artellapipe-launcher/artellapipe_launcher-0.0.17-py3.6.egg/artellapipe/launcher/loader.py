#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for artellapipe-launcher
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import inspect
import logging.config

import tpDcc as tp


def init(do_reload=False, dev=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """

    from tpDcc.libs.python import importer
    from artellapipe.launcher import register

    logger = create_logger()
    register.register_class('logger', logger)

    if not dev:
        import sentry_sdk
        try:
            sentry_sdk.init("https://c329025c8d5a4e978dd7a4117ab6281d@sentry.io/1770788")
        except RuntimeError:
            sentry_sdk.init("https://c329025c8d5a4e978dd7a4117ab6281d@sentry.io/1770788", default_integrations=False)

    class ArtellaLauncher(importer.Importer, object):
        def __init__(self, debug=False):
            super(ArtellaLauncher, self).__init__(module_name='artellapipe.launcher', debug=debug)

        def get_module_path(self):
            """
            Returns path where tpNameIt module is stored
            :return: str
            """

            try:
                mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
            except Exception:
                try:
                    mod_dir = os.path.dirname(__file__)
                except Exception:
                    try:
                        import artellapipe.launcher
                        mod_dir = artellapipe.launcher.__path__[0]
                    except Exception:
                        return None

            return mod_dir

    packages_order = []

    launcher_importer = importer.init_importer(importer_class=ArtellaLauncher, do_reload=False, debug=dev)
    launcher_importer.import_packages(order=packages_order, only_packages=False)
    if do_reload:
        launcher_importer.reload_all()

    register_resources()


def create_logger():
    """
    Returns logger of current module
    """

    logging.config.fileConfig(get_logging_config(), disable_existing_loggers=False)
    logger = logging.getLogger('artellapipe-launcher')

    return logger


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """

    artellapipe_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'artellapipe', 'logs'))
    if not os.path.isdir(artellapipe_logger_dir):
        os.makedirs(artellapipe_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    create_logger_directory()

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def get_logging_level():
    """
    Returns logging level to use
    :return: str
    """

    if os.environ.get('ARTELLAPIPE_LAUNCHER_LOG_LEVEL', None):
        return os.environ.get('ARTELLAPIPE_LAUNCHER_LOG_LEVEL')

    return os.environ.get('ARTELLAPIPE_LAUNCHER_LOG_LEVEL', 'DEBUG')


def register_resources():
    """
    Registers artellapipe-launcher resources
    """

    resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
    tp.ResourcesMgr().register_resource(resources_path, 'launcher')
