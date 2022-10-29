import os

MaxTasks = 1
Sleep = 1

SmtpAuth = {
    'hostname': 'smtp.gmail.com',
    'username': os.getenv('Env_SmtpUser'),
    'password': os.getenv('Env_SmtpPassw'),
    'port': 465,
    'use_tls': True
}

From = 'ua0976646510@gmail.com'
