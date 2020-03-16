# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from argparse import ArgumentParser
import yaml
import sys
import logging
import importlib
import os
import zipfile
import json
import re
import uuid


logging.basicConfig(
    level='INFO',
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%y%m%d %H:%M:%S'
)


class SparkJob(object):

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

    def zipdir(self, path, ziph, excludes=r'(.venv/)'):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file_ in files:
                _fname = os.path.join(root, file_)[len(path):]
                if excludes and re.findall(
                        excludes, _fname, re.IGNORECASE):
                    continue
                if file_.endswith('.py'):
                    ziph.write(
                        os.path.join(root, file_),
                        os.path.join(root, file_)[len(path):])

    def _configure_logger(self):
        log_level = self.configs.get('log-level', 'INFO').upper()
        config_path = os.path.join(self.job_path, 'config.yaml')

        self.logger = logging.getLogger()
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

    def _configure_spark(self):
        app_name = self.configs.get('app-name', 'app')
        log_level = self.configs.get('log-level', 'INFO').upper()

        conf = SparkConf().setAppName(app_name)
        self.sc = SparkContext(conf=conf)
        self.sc.setLogLevel(log_level)
        self.spark = SparkSession.builder.appName(
            'spark-session').getOrCreate()

    def _configure_include_paths(self):
        include_paths = self.configs.get('include_paths')
        if not include_paths:
            include_paths = []
        elif isinstance(include_paths, str):
            include_paths = [include_paths]

        include_paths.append(self.job_path)

        if include_paths:
            self.temp_files = []
            logging.info(
                'Adding {} to PYTHONPATH'.format(','.join(include_paths)))
            for ix, _path in enumerate(include_paths):
                _zip_filename = '.dep.{}.zip'.format(uuid.uuid4().hex[: 8])
                self.logger.info('Zip directory {}'.format(_path))
                zipf = zipfile.ZipFile(
                    _zip_filename, 'w', allowZip64=True)
                self.zipdir(_path, zipf)
                zipf.close()
                self.sc.addPyFile(
                    os.path.join(self.job_path, _zip_filename))
                self.temp_files.append(_zip_filename)
            include_paths.extend(sys.path)
            sys.path = include_paths

    def configure(self):

        self._configure_logger()
        self._configure_spark()
        self._configure_include_paths()

        self._main_function = SparkJob._get_function(
            self.configs.get('entry'))

    def run(self):

        self._main_function(self)

    def cleanup(self):
        if hasattr(self, 'temp_files'):
            for f in getattr(self, 'temp_files'):
                os.remove(f)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('params')
    options = parser.parse_args()
    loader = SparkJob(options.path, options.params)
    loader.run()
    loader.cleanup()
