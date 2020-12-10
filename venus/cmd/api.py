# Copyright 2020 Inspur
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Starter script for Venus OS API."""

import eventlet
import os
import sys

from oslo_config import cfg
from oslo_log import log as logging
from oslo_reports import guru_meditation_report as gmr

from venus.common import config  # noqa
from venus import i18n
from venus import objects
from venus import service
from venus import utils
from venus import version

eventlet.monkey_patch()
i18n.enable_lazy()

CONF = cfg.CONF


def main():
    objects.register_all()
    CONF(sys.argv[1:], project='venus',
         version=version.version_string())
    logdir = CONF.log_dir
    is_exits = os.path.exists(logdir)
    if not is_exits:
        os.makedirs(logdir)
    logging.setup(CONF, "venus")
    utils.monkey_patch()

    gmr.TextGuruMeditation.setup_autorun(version)

    launcher = service.get_launcher()
    server = service.WSGIService('osapi_venus')
    launcher.launch_service(server, workers=server.workers)
    launcher.wait()


if __name__ == "__main__":
    main()
