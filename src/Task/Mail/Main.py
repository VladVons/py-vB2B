# Created: 2022.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

'''
from Task.Mail.Main import TMail, TMailSmtp, TMailConf, TMailSend

Mail = TEMail(
    TMailSmtp(
        username = 'xxx',
        password = 'xxx'
    ),
    TMailConf(
        MaxTasks = 5
    )
)

for i in range(3):
    MailSend = TMailSend(
        From = 'your@gmail.com',
        To = 'email@gmail.com',
        Subject = f'TMail test no {i}',
        Body = 'Hello\n'
    )
    Mail.Add(MailSend)
Mail.Run()
'''


import asyncio
import aiosmtplib
#
from Inc.DataClass import DataClass
from Inc.Misc.Mail import TMail, TMailSmtp, TMailSend
from IncP.Log import Log


@DataClass
class TMailConf():
    Sleep: int = 3
    MaxTasks: int = 5
    Always: bool = False


class TEMail():
    def __init__(self, aMailSmtp: TMailSmtp, aMailConf: TMailConf):
        self._MailConf = aMailConf
        self._CntDone = 0
        self._Queue = asyncio.Queue()
        self._Mail = TMail(aMailSmtp)
        self.IsRun = False

    async def _DoPost(self, _aOwner, aMsg):
        if (aMsg.get('To') == self.__class__.__name__):
            if (aMsg.get('type') == 'add'):
                self.Add(aMsg.get('mail_send'))

    def Add(self, aMailSend: TMailSend):
        self._Queue.put_nowait(aMailSend)

    async def Send(self, aData: TMailSend):
        await self._Mail.Send(aData)
        Log.Print(1, 'i', 'MailTo:%s, Done:%d' % (aData.To, self._CntDone))

    async def _Worker(self, aTaskId: int):
        await asyncio.sleep(aTaskId)

        self.IsRun = True
        while (self.IsRun):
            await asyncio.sleep(self._MailConf.Sleep)
            if (not self._Queue.empty()):
                try:
                    MailSend: TMailSend = await asyncio.wait_for(self._Queue.get(), timeout = 0.5)
                except asyncio.exceptions.TimeoutError:
                    continue

                try:
                    if (MailSend.Lock):
                        async with MailSend.Lock:
                            await self.Send(MailSend)
                    else:
                        await self.Send(MailSend)
                    self._CntDone += 1
                except aiosmtplib.errors.SMTPDataError as E:
                    Log.Print(1, 'x', 'Err:%s, %s' % (MailSend.To, E))
                    await asyncio.sleep(self._MailConf.Sleep * 10)
                finally:
                    self._Queue.task_done()
            elif (not self._MailConf.Always):
                break

    async def Run(self):
        Log.Print(1, 'i', 'TMail.Run() start')
        Tasks = [
            asyncio.create_task(self._Worker(i))
            for i in range(self._MailConf.MaxTasks)
        ]
        await asyncio.gather(*Tasks)
        self.IsRun = False
        Log.Print(1, 'i', 'TMail.Run() finish')
