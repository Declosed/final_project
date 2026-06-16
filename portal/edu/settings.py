# eduportal/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eduportal_db',          # Your MySQL database name
        'USER': 'portal_root',           # Your MySQL database user
        'PASSWORD': 'SecureMySqlPassword2026!',
        'HOST': '127.0.0.1',             # MySQL server address
        'PORT': '3306',                  # Default MySQL port
        'OPTIONS': {
            # Standard isolation levels to handle concurrent high-volume attendance hits safely
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
