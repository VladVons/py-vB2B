# Created: 2022.10.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGet
from Inc.UtilP.Mail import TMailSmtp
from .Main import TEMail, TMailConf

#Enable = False

def Main(aConf) -> tuple:
    Obj = TEMail(
        TMailSmtp(
            username = DeepGet(aConf, 'SmtpAuth.username'),
            password = DeepGet(aConf, 'SmtpAuth.password')
        ),
        TMailConf(
            MaxTasks = aConf.get('MaxTasks', 1),
            Sleep = aConf.get('Sleep', 3),
            Always = True
        )
    )
    return (Obj, Obj.Run())
