# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals
import yaml
import sys
import logging
import importlib
import os
import json


logging.basicConfig(
    level='INFO',
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%y%m%d %H:%M:%S'
)


class BaseJob(object):

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
        logging.info('Use function `{}`'.format(name))
        _module, _function = name.rsplit(':', 1)
        _module = importlib.import_module(_module)
        return getattr(_module, _function)

    def configure(self):

        log_level = self.configs.get('log-level', 'INFO').upper()
        config_path = os.path.join(self.job_path, 'config.yaml')

        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(
            getattr(
                logging,
                log_level))
        self.logger.info(
            'Loading config from {}'.format(config_path))

        self._main_function = BaseJob._get_function(
            self.configs.get('entry'))

    def run(self):

        self._main_function(self)