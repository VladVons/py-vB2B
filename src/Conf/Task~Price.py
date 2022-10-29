import os


SendMail = {
    'SmtpAuth': {
        'hostname': 'smtp.gmail.com',
        'username': os.getenv('Env_SmtpUser'),
        'password': os.getenv('Env_SmtpPassw'),
        'port': 465,
        'use_tls': True
    }
}
