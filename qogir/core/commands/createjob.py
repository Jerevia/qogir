from __future__ import absolute_import, print_function

from qogir.core.commands import BaseCommand, CommandError
import re
import os
import qogir
import shutil


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'name', metavar='name',
            help='Name of app',
        )

        parser.add_argument(
            '--type', metavar='type',
            default='default',
            choices=['default', 'pyspark'],
            help='Type of app'
        )


    def _is_valid_name(self, name):
        if not re.match(r'^[a-zA-Z]+[\w_]+$', name):
            raise CommandError('Invalid project name')

    def check(self):
        pass

    def execute(self, **options):
        name = options.get('name')
        _type = options.get('type')

        self._is_valid_name(name)
        _template_dir = os.path.join(
            qogir.__path__[0], 'templates', '{}_job_template'.format(_type))

        shutil.copytree(_template_dir, name)

        for dir_name, subdir_list, file_list in os.walk(name):
            for _file in file_list:
                if not _file.endswith('.tpl'):
                    continue
                shutil.move(
                    os.path.join(dir_name, _file),
                    os.path.join(dir_name, _file[:-4]),
                    )

        print('Successfully create project {}'.format(name))
