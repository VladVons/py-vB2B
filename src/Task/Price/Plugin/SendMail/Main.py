# Created: 2022.10.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGet, Filter
from Inc.PluginTask import Plugin
from Inc.UtilP.Mail import TMail, TMailSmtp, TMailSend
from IncP import GetInfo
from ..Common import TFileBase


class TMain(TFileBase):
    async def Run(self):
        Info = [
            f'{Key}: {Val}'
            for Key, Val in sorted(GetInfo().items())
        ]

        ConfTask, _ = Plugin.GetConf('Task.Price')
        ConfSmtp = DeepGet(ConfTask, 'SendMail.SmtpAuth')
        Mail = TMail(TMailSmtp(**ConfSmtp))
        Filtered = Filter(self.Parent.Conf, ['From', 'To', 'Subject', 'Body', 'File'])
        Filtered['Body'] += '\n---\n'+ '\n'.join(Info)
        Data = TMailSend(**Filtered)
        await Mail.Send(Data)
