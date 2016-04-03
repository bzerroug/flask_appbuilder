import os
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h'

# The SQLAlchemy connection string.

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_BINDS = {
    'postgresql' : 'postgresql://dataware-ro:jAsPM3xE9ul9WFi@10.230.0.140:5432/dataware'
}


# Flask-WTF flag for CSRF
CSRF_ENABLED = True


APP_NAME = "Meteo Auchan Direct"


# AUTHENTICATION CONFIG

AUTH_TYPE = AUTH_DB

# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Public"

AUTH_TYPE = 1 # Database Authentication
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Public'
# Config for Flask-Mail necessary for user registration
MAIL_SERVER = '***'
MAIL_USE_TLS = True
MAIL_USERNAME = 'yourappemail@gmail.com'
MAIL_PASSWORD = 'passwordformail'
MAIL_DEFAULT_SENDER = '***'


# Babel config for translations
BABEL_DEFAULT_LOCALE = 'en'

# Your application default translation path
BABEL_DEFAULT_FOLDER = 'translations'

# The allowed translation for you app
LANGUAGES = {
    'en': {'flag':'gb', 'name':'English'},
    'pt': {'flag':'pt', 'name':'Portuguese'},
    'pt_BR': {'flag':'br', 'name': 'Pt Brazil'},
    'es': {'flag':'es', 'name':'Spanish'},
    'de': {'flag':'de', 'name':'German'},
    'zh': {'flag':'cn', 'name':'Chinese'},
    'ru': {'flag':'ru', 'name':'Russian'},
    'pl': {'flag':'pl', 'name':'Polish'}
}

# The file upload folder, when using models with files
UPLOAD_FOLDER = basedir + '/app/static/uploads/'

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/'

# The image upload url, when using models with images
IMG_UPLOAD_URL = '/static/uploads/'
# Setup image size default is (300, 200, True)
#IMG_SIZE = (300, 200, True)

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
#APP_THEME = "bootstrap-theme.css"  # default bootstrap
#APP_THEME = "cerulean.css"
#APP_THEME = "amelia.css"
#APP_THEME = "cosmo.css"
#APP_THEME = "cyborg.css"  
#APP_THEME = "flatly.css"
#APP_THEME = "journal.css"
#APP_THEME = "readable.css"
#APP_THEME = "simplex.css"
#APP_THEME = "slate.css"   
#APP_THEME = "spacelab.css"
#APP_THEME = "united.css"
#APP_THEME = "yeti.css"



DB={
"HOST_DB" : "10.230.0.140",
"PORT_DB" : "5432",
"USER_DB" : "dataware-ro",
"PASS_DB" : "jAsPM3xE9ul9WFi",
"DATABASE_DB" : "dataware"
}

splunk_conf={
"host_splunk" : "94.124.133.189",
"port_splunk" : "8089",
"username_splunk" : "bzerroug",
"password_splunk" : "Bachir2015"
}

GA_conf={
"client_idGA" : "304171817884-l0utird51gdsn4jilaf4dbao7fki0ul9.apps.googleusercontent.com",
"project_idGA" : "teak-proton-121517",
"auth_uriGA" : "https://accounts.google.com/o/oauth2/auth",
"token_uriGA" : "https://accounts.google.com/o/oauth2/token",
"auth_provider_x509_cert_urlGA" : "https://www.googleapis.com/oauth2/v1/certs",
"client_secretGA" : "M41z9gE0jRc4Go8jkI8NNnm6",
"redirect_urisGA" : ["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
}
