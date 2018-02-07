from home.utils import encrypt
from jinja2 import Template
from getpass import getpass
import sys

template_smtp = """
[EMAIL]
HOST = {{ host }}
PORT = {{ port }}
USER = {{ host_user }}
FROM = {{ default_from_email }}
TLS = {{ use_tls }}
"""


def run(*args):
    print("Server SMTP :")
    host = input('host : ')
    port = input('port : ')
    host_user = input('user : ')
    host_password = getpass('password : ')
    default_from_email = input('default from email : ')
    use_tls = input('The SMTP host use TLS ? : (True/False) ')

    t = Template(template_smtp)
    final = t.render(host=host,
                     port=port,
                     host_user=host_user,
                     default_from_email=default_from_email,
                     use_tls=str(use_tls)
                     )

    with open(args[0] + 'conf.ini', 'a', encoding='utf_8') as f:
        f.write(final)
    with open(args[0] + 'password_email.txt', 'w', encoding='utf_8') as f:
        f.write(encrypt(host_password).decode('utf-8'))
    sys.exit(0)
