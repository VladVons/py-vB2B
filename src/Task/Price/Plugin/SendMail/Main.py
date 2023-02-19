# Created: 2022.10.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGet, Filter
from Inc.Misc.Mail import TMail, TMailSmtp, TMailSend
from Inc.ParserX.Common import TFileBase
from IncP import GetInfo
from Task import Plugin


class TMain(TFileBase):
    async def Run(self):
        Info = [
            f'{Key}: {Val}'
            for Key, Val in sorted(GetInfo().items())
        ]

        ConfTask, _ = Plugin.GetConf('Price')
        ConfSmtp = DeepGet(ConfTask, 'send_mail.smtp_auth')
        Mail = TMail(TMailSmtp(**ConfSmtp))
        Filtered = Filter(self.Parent.Conf, ['mail_from', 'mail_to', 'mail_subject', 'mail_body', 'file'])
        Filtered['mail_body'] += '\n---\n'+ '\n'.join(Info)
        Data = TMailSend(**Filtered)
        await Mail.Send(Data)
