# Created: 2022.05.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
#
from .FormBase import TFormBase
from ..Session import Session


class TForm(TFormBase):
    Title = 'Login'

    UserName = StringField(validators = [DataRequired(), Length(min=1, max=32)], render_kw = {'placeholder': 'login'})
    Password = PasswordField(validators = [Length(min=1, max=16)], render_kw = {'placeholder': 'password'})
    Submit = SubmitField("ok")

    async def _Render(self):
        self.Data.Message = '%s (%s)' % (Session.Data.get('UserName'), Session.Data.get('UserGroup', ''))
        self.Data.Query = self.Request.query_string
        if (not self.validate()):
            return

        Conf = self.Parent.Parent.Conf
        if (self.UserName.data != Conf.get('User')) and (self.Password.data != Conf.get('Password')):
            self.Data.Message = 'Authorization failed for %s' % (self.UserName.data)
            return

        Session.Data.update({'UserId': 1, 'UserName': self.UserName.data})

        Redirect = self.Request.query.get('url', '/')
        raise web.HTTPFound(location = Redirect)
