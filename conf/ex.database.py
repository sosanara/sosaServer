def database():
    return {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'database',
            'USER': 'db_id',
            'PASSWORD': 'db_password',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        }
    }
