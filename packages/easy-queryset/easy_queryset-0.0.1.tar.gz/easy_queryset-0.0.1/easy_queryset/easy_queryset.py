from django.conf import global_settings, settings
import django
settings.configure(DEBUG=True)
django.setup()


def add_mysql(host, user, password, db, port=3306, app_label="default"):
    global_settings.DATABASES = {
        app_label: {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
    }


def add_postgresql(host, user, password, db, port=3306, app_label="default"):
    global_settings.DATABASES = {
        app_label: {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
    }


def add_sqlite(name, app_label="default"):
    global_settings.DATABASES = {
        app_label: {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': name,
        }
    }


def add_oracle(host, user, password, db, port=3306, app_label="default"):
    global_settings.DATABASES = {
        app_label: {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': db,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
    }
