# ==========================================
# DATABASE CONFIGURATION
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Declosed',          # Matches the schema name initialized in Workbench
        'USER': 'root',                  # Your MySQL root administrative user account 
        'PASSWORD': 'Declosed@9333', # Your exact MySQL login password
        'HOST': '127.0.0.1',             # Standard local loop network host location
        'PORT': '3306',                  # Default system assignment communication port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}  
