# This file is a part of Dramatiq.
#
# Copyright (C) 2017,2018 CLEARTYPE SRL <bogdan@cleartype.io>
#
# Dramatiq is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# Dramatiq is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import

import sys
import inspect
import logging

default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))


# @danilo here: shamelessly copied from Flask.
def has_level_handler(logger):
    level = logger.getEffectiveLevel()
    current = logger
    while current:
        if any(handler.level <= level for handler in current.handlers):
            return True
        if not current.propagate:
            break
        current = current.parent
    return False


def get_logger(module, name=None, level=None):
    logger_fqn = module
    if name is not None:
        if inspect.isclass(name):
            name = name.__name__
        logger_fqn += "." + name
    logger = logging.getLogger(logger_fqn)
    # level
    if logger.level == logging.NOTSET:
        logger.setLevel(level or logging.DEBUG)
    # handler
    if not has_level_handler(logger):
        logger.addHandler(default_handler)

    return logger
