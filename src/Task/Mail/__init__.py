# Created: 2022.10.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGet
from Inc.Misc.Mail import TMailSmtp
from .Main import TEMail, TMailConf

#Enable = False

def Main(aConf) -> tuple:
    Obj = TEMail(
        TMailSmtp(
            username = DeepGet(aConf, 'smtp_auth.username'),
            password = DeepGet(aConf, 'smtp_auth.password')
        ),
        TMailConf(
            MaxTasks = aConf.get('max_tasks', 1),
            Sleep = aConf.get('sleep', 3),
            Always = True
        )
    )
    return (Obj, Obj.Run())
