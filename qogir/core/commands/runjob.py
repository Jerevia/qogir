from __future__ import absolute_import, print_function

from qogir.core.commands import BaseCommand, CommandError
from qogir.core.runner import JobRunner
from subprocess import Popen, PIPE
import re
import os
import qogir
import shutil
import sys
import logging
import yaml

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    datefmt='%y%m%d %H:%M:%S'
)


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            'path', metavar='Path',
            help='Job path',
        )

        parser.add_argument(
            '--params', '-P', metavar='params',
            default=None,
            help='Params of the job, must be json',
        )

    def check(self):
        pass

    @staticmethod
    def run_bash_command(command):
        proc = Popen(
            command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            executable='/bin/bash',
            shell=True,
        )
        proc.communicate()
        if proc.returncode != 0:
            raise CommandError('Command finished with a nonzero return code.')

    def execute(self, **options):
        path = os.path.abspath(options['path'])
        params = options['params']
        runner = JobRunner(path)
        runner.run(params=params)
