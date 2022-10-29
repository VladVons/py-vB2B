# Created: 2022.04.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from wtforms.fields import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Email
#
from Inc.PluginTask import Plugin
from Inc.UtilP.FS import DirRemove
from Inc.UtilP.Zip import Extract
from Task.Price.Main import TPrice
from Task.Queue.Main import TCall
from .FormBase import TFormBase
from ..Common import FileWriter


class TForm(TFormBase):
    Title = 'Price list'

    EMail = StringField(validators = [DataRequired(), Email('eMail check')], render_kw = {'placeholder': 'eMail'})
    File = FileField(validators=[DataRequired()])
    Submit = SubmitField('ok')

    async def _Render(self):
        if (not await self.PostToForm()):
            return

        if (not self.validate()):
            Err = self.File.errors + self.EMail.errors
            self.Data.Message = ','.join(Err)
            return

        Parent = self.Parent.Parent
        FileDownload = f'{Parent.DirRoot}/{Parent.DirDownload}/{self.File.data.filename}'
        Len = await FileWriter(self.File.data.file, FileDownload)
        if (Len == 0) or (self.File.data.content_type != 'application/zip'):
            self.Data.Message = f'Not a zip file {self.File.data.file}'
            return

        ConfDirPrice = Parent.Conf.get('DirPrice')
        if (os.path.exists(ConfDirPrice)):
            DirRemove(ConfDirPrice)
        else:
            os.makedirs(ConfDirPrice, exist_ok=True)

        Extract(FileDownload, ConfDirPrice)

        await Plugin.Post(Parent, {
            'To': 'TQueue',
            'Type': 'Add',
            'Call': TCall(TPrice().Run, [{
                'SendMail': {'To': [self.EMail.data]}
            }])
        })

        self.Data.Message = f'Check for a while {self.EMail.data}'
