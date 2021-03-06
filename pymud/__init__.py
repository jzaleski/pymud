import os

from os.path import (
    abspath,
    dirname,
    isfile,
    join as join_path,
)

from six.moves.configparser import ConfigParser

from pymud.utilities import ConsoleLogger


rel_path = abspath(join_path(dirname(__file__), 'pymud.conf'))
etc_path = join_path('/etc/pymud', 'pymud.conf')

CONFIG = ConfigParser()

if isfile(rel_path):
    CONFIG.read(rel_path)
elif isfile(etc_path):
    CONFIG.read(etc_path)
else:
    CONFIG.add_section('general')
    CONFIG.set(
        'general',
        'host',
        os.getenv('HOST', '0.0.0.0')
    )
    CONFIG.set(
        'general',
        'port',
        os.getenv('PORT', '7001')
    )

LOGGER = ConsoleLogger()
