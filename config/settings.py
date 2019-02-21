import secrets
from os import environ as env

# Flask config
IP = env.get('IP', '0.0.0.0')
PORT = env.get('PORT', 8080)

SECRET_KEY = env.get("SECRET_KEY", default='Back Door')
FLAG = env.get("FLAG", default='Not Set')