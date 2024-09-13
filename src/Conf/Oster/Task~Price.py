from Inc.Misc.Env import GetEnvWithWarn
from IncP.Log import Log


send_mail = {
    'smtp_auth': {
        'hostname': 'smtp.gmail.com',
        'username': GetEnvWithWarn('env_smtp_user', Log),
        'password': GetEnvWithWarn('env_smtp_passw', Log),
        'port': 465,
        'use_tls': True
    }
}
