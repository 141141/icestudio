#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Install icestorm toolchain in Icestudio path using apio
# March 2016
# GPLv2

import sys
import shutil
import subprocess

from platform import system
from os.path import isdir, join, expanduser, normpath, dirname, abspath

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'


VIRTUALENV = join(dirname(abspath(__file__)), 'virtualenv-14.0.1')
ICESTUDIO_PATH = join('/custom/click/com.ubuntu.puritine/0.6/libertine-data/libertine-container/puritine/rootfs/home/', '.icestudio')
if system() == 'Windows':
    ICESTUDIO_BIN = join(ICESTUDIO_PATH, 'Scripts')
else:
    ICESTUDIO_BIN = join(ICESTUDIO_PATH, 'bin')
ICESTUDIO_PIP = join(ICESTUDIO_BIN, 'pip')
ICESTUDIO_APIO = join(ICESTUDIO_BIN, 'apio')
PYTHON_EXE = normpath(sys.executable)

def run(commands):
    result = {
        'out': None,
        'err': None,
        'returncode': None}

    p = subprocess.Popen(
        commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=system() == 'Windows')

    try:
        result['out'], result['err'] = p.communicate()
        result['returncode'] = p.returncode
    except KeyboardInterrupt:
        print('Aborted by user')
        sys.exit(1)

    if result['returncode'] != 0:
        print >> sys.stderr, ' '.join(commands)
        sys.exit(1)

    return result

run([PYTHON_EXE, '--version'])

# $ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
# $ tar xvfz virtualenv-X.X.tar.gz

if isdir(ICESTUDIO_PATH):
    shutil.rmtree(ICESTUDIO_PATH)

print 1

run([PYTHON_EXE, join(VIRTUALENV, 'virtualenv.py'), ICESTUDIO_PATH])

print 2

run([ICESTUDIO_PIP, 'install', '-U', 'apio'])

print 3

run([ICESTUDIO_APIO, '--version'])

print 4

run([ICESTUDIO_APIO, 'install'])
