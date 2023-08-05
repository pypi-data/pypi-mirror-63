######################################
# as compiler configurations default
######################################
from __future__ import absolute_import, division, print_function

from parts.config import *


def map_default_version(env):
    return env['BINUTILS_VERSION']


config = configuration(map_default_version)

config.VersionRange("2-*",
                    prepend=ConfigValues(
                        ASPPFLAGS=['-m64']
                    )
                    )
