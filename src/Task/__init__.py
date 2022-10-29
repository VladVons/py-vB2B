# Created: 2022.10.12
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from Inc.Conf import TConf


ConfTask = TConf('Conf/Task.py')
ConfTask.Load()
ConfTask.Def = {'Env_EmailPassw': os.getenv('Env_EmailPassw')}
