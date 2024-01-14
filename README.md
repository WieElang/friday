# Task Management App Admin Friday

## Setup Project
1. Install python3

2. Install virtualenv
   run command `pip install virtualenv`

3. Install yarn

4. Create Environment
   run command `python -m venv /path/to/new/virtual/environment`

5. Activate Environment
   run command `source <venv>/bin/activate`

6. Install requirement
   run command `pip install -r requirements.txt`

7. Setup database
   Fill your database config in `settings_local.py` file
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'friday',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'friday_test',
        },
    }
}
```

8. Migrate all migrations
   run command `migrate.py migrate`

9. Collectstatic file
   run command `migrate.py collectstatic`

10. Create superuser
   run command `migrate.py createsuperuser`

11. Run application
   run command `migrate.py runserver`
