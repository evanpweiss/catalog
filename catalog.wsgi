import sys

sys.path.append('/var/www/catalog')

from project import app as application

application.secret_key = "super_secret_key"
