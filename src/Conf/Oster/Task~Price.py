from Inc.UtilP.Misc import GetEnvWithWarn
from IncP.Log import Log


SendMail = {
    'SmtpAuth': {
        'hostname': 'smtp.gmail.com',
        'username': GetEnvWithWarn('Env_SmtpUser', Log),
        'password': GetEnvWithWarn('Env_SmtpPassw', Log),
        'port': 465,
        'use_tls': True
    }
}
