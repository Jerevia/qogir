
from qogir.core.commands import BaseCommand, CommandError
from qogir.utils.commands import run_bash_command

import os
import logging
import qogir
import yaml
import aiofiles
import asyncio
import json
import sys


class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass


class AsyncJobRunner(aobject):

    async def __init__(self, path, **kwargs):
        if not os.path.exists(os.path.join(path, '.qogir')):
            raise CommandError('Invalid Job Path')
        self.root_dir = qogir.__path__[0]
        self.path = os.path.abspath(path)
        self.env = os.path.join(self.path, '.venv')
        self.params = None
        config_path = os.path.join(path, 'config.yaml')
        async with aiofiles.open(config_path) as f:
            self.config = yaml.load(await f.read())

    async def configure(self):
        job_type = self.config['job-type']
        self.command_ = await getattr(
            self, 'get_{}_command'.format(job_type))()

    async def get_default_command(self):
        tpl_path = os.path.join(
            self.root_dir,
            'templates', 'default.submit.sh.tpl')
        runner_path = os.path.join(
            self.root_dir,
            'core', 'jobs', 'default.py')
        _command = open(tpl_path).read()
        _command = _command.format(
            job_path=self.path,
            env=self.env,
            runner_path=runner_path,
            params=self.params
        )
        return _command

    async def get_pyspark_command(self):

        tpl_path = os.path.join(
            self.root_dir, 'templates', 'pyspark.submit.sh.tpl')
        runner_path = os.path.join(
            self.root_dir, 'core', 'jobs', 'pyspark_.py')
        spark_python_path = os.path.join(
            self.env, 'bin', 'python')
        submit_exec_path = os.path.join(
            self.env, 'bin', 'spark-submit')
        _command = open(tpl_path).read()
        _command = _command.format(
            job_path=self.path,
            env_path=self.env,
            runner_path=runner_path,
            submit_exec_path=submit_exec_path,
            spark_python_path=spark_python_path,
            params=self.params,
            **self.config['command-params'])
        return _command

    async def _check_venv(self):
        _include_paths = self.config.get('include_paths')
        if not _include_paths:
            include_paths = []
        else:
            if isinstance(_include_paths, str):
                _include_paths = [_include_paths]
            include_paths = [repr(
                _path) for _path in _include_paths]
        tpl_path = os.path.join(
            self.root_dir,
            'templates', 'check_venv.sh.tpl')
        async with aiofiles.open(tpl_path) as f:
            _command = await f.read()
        _command = _command.format(
            job_path=self.path,
            python=self.config['python'],
            include_paths=' '.join(include_paths))
        if await self.run_bash_command(_command) != 0:
            raise CommandError(
                'Command finished with a nonzero return code.')

    async def run(self, *args, **kwargs):
        self.params = None
        if 'params' in kwargs:
            if isinstance(kwargs['params'], dict):
                self.params = json.dumps(kwargs['params'])
            else:
                self.params = kwargs['params']
        await self.configure()
        await self._check_venv()
        if await self.run_bash_command(self.command_) != 0:
            raise CommandError(
                'Command finished with a nonzero return code.')

    async def run_bash_command(self, cmd):
        asyncio.subprocess.PIPE = sys.stdout
        proc = await asyncio.create_subprocess_shell(
            cmd)
        await proc.communicate()
        return proc.returncode