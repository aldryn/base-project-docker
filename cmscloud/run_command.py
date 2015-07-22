#-*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import subprocess32 as subprocess  # backport of python3 subprocess with timeout support


def run_command(command):
    timeout = 30
    try:
        return {
            'returncode': 0,
            'cmd': command,
            'output': subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            ),
        }
    except subprocess.CalledProcessError as e:
        # TODO: kill any subprocesses that might still be around
        return {
            'returncode': e.returncode,
            'cmd': command,
            'output': e.output,
            'error': e.message,
        }
    except subprocess.TimeoutExpired as e:
        # TODO: kill any subprocesses that might still be around
        return {
            'returncode': None,
            'cms': command,
            'output': e.output,
            'error': e.message,
            'note': 'timeout!'
        }

