from __future__ import absolute_import, print_function, unicode_literals
from subprocess import Popen
import sys


def run_bash_command(command):
    proc = Popen(
        command,
        executable='/bin/bash',
        shell=True,
    )
    proc.communicate()
    return proc.returncode
