# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals
from argparse import ArgumentParser
import yaml
import sys
import logging
import importlib
import os
import json
import pkg_resources


logging.basicConfig(
    level='INFO',
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%y%m%d %H:%M:%S'
)


class DefaultJob(object):

    def __init__(self, path, params):
        os.chdir(path)
        config_path = os.path.join(path, 'config.yaml')
        sys.path.insert(0, path)

        self.job_path = path
        with open(config_path) as f:
            self.configs = yaml.load(f)

        self.params = {}
        if params != 'None':
            self.params = json.loads(params)
        self.configure()

    @staticmethod
    def _get_function(name):
        logging.info('Using function `{}`'.format(name))
        _module, _function = name.rsplit(':', 1)
        _module = importlib.import_module(_module)
        return getattr(_module, _function)

    def configure(self):
        include_paths = self.configs.get('include_paths')
        if not include_paths:
            include_paths = []
        elif isinstance(include_paths, str):
            include_paths = [include_paths]

        include_paths.append(self.job_path)
        log_level = self.configs.get('log-level', 'INFO').upper()
        config_path = os.path.join(self.job_path, 'config.yaml')

        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(
            getattr(
                logging,
                log_level))
        self.logger.info(
            'Loading config from {}'.format(config_path))
        __builtins__.d = self.logger.debug
        __builtins__.i = self.logger.info
        __builtins__.w = self.logger.warning
        __builtins__.e = self.logger.error

        if include_paths:
            include_paths = list(
                map(lambda x: os.path.abspath(x), include_paths))
            logging.info(
                'Adding {} to PYTHONPATH'.format(','.join(include_paths)))
            include_paths.extend(sys.path)
            sys.path = include_paths

        self._main_function = DefaultJob._get_function(
            self.configs.get('entry'))

    def run(self):

        self._main_function(self)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('params')
    options = parser.parse_args()
    loader = DefaultJob(options.path, options.params)
    loader.run()
