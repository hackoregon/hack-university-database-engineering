# Python ORM

This was an activity based class, so there wasn't a solid lesson plan.  The assignment at the end was the challenge for the class.  The other notes were things that helped get there.  The assignment was done in groups based on project teams.


install miniconda (this is the aspiring hack oregon standard)

All of this happens underneath a user account and not at the system level.

install jupyter (not from a virtual environment)
```
conda install jupyter
```

create virtual environment
```
conda create -n cvdjango python django psycopg2
```

delete virtual environment (if you need)
```
conda remove -n cvdjango --all
```

Activate virtual environment
```
source activate cvdjango
```

Install more requirements (make sure that you activate the environment first)
```
pip install djangorestframework
```

create django project
```
django-admin startproject ORM ~/proj/django
```

setup a db for django and put a (super low security) password on vagrant
```sql
CREATE DATABASE django;
ALTER USER vagrant WITH PASSWORD 'vagrant';
```

Modify settings.py (under ~/proj/django)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Assignment

1. Create models that correspond to schools.csv and view them in the django admin interface.
2. Load schools.csv into those models.
3. Repeat 1 and 2 for performance.csv
4. Create restful endpoints for the two models.
5. Create a third restful endpoint that joins the two models together.
