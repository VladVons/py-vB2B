from Inc.UtilP.Misc import GetEnvWithWarn
from IncP.Log import Log


MaxTasks = 1
Sleep = 1

SmtpAuth = {
    'hostname': 'smtp.gmail.com',
    'username': GetEnvWithWarn('Env_SmtpUser', Log),
    'password': GetEnvWithWarn('Env_SmtpPassw', Log),
    'port': 465,
    'use_tls': True
}

From = 'ua0976646510@gmail.com'
