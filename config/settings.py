import secrets
from os import environ as env

# Flask config
IP = env.get('IP', '127.0.0.1')
PORT = env.get('PORT', 5000)

SECRET_KEY = env.get("SECRET_KEY", default='Back Door')
FLAG = env.get("FLAG", default='Not Set')