from Inc.Misc.Env import GetEnvWithWarn
from IncP.Log import Log


max_tasks = 1
sleep = 1

smtp_auth = {
    'hostname': 'smtp.gmail.com',
    'username': GetEnvWithWarn('env_smtp_user', Log),
    'password': GetEnvWithWarn('env_smtp_passw', Log),
    'port': 465,
    'use_tls': True
}
