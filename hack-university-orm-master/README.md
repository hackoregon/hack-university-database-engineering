# hack-university-orm
Intro to Object-relational mapping (ORM)

### Class Notes
[Class Notes](class_notes.md)

#### A note for the vagrant box users
I had to make the following modifications to the vagrant image:

 - `ssh-keygen` and add the id_rsa.pub to my github profile to git clone
 - sudo apt-get update
 - sudo apt-get upgrade
 - sudo apt-get install libpq-dev postgresql-client-common python-virtualenv
 - set up the vagrant user for access to postgres:
    - sudo su - postgres
    - createuser vagrant -s P
        - set the password to `vagrant`
    - exit
 - createdb vagrant


## Quick start

```console
# get the repo
git clone https://github.com/hackoregon/hack-university-orm.git
cd hack-university-orm

# create and activate the python virtual environment 
virtualenv .virt
source .virt/bin/activate
# note if you're running this from the vagrant image, then you may need to install virtualenv: `sudo apt-get install virtualenv`

# install the python requirements and dependencies
pip install -U pip
pip install -r requirements.txt

# create the database and run migrations
createdb orms
cd orms
python manage.py migrate
```

The `migrate` command will produce output similar to:
```console
Operations to perform:
  Apply all migrations: admin, contenttypes, auth, sessions
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying sessions.0001_initial... OK
```

#### Congrats!
You've set up the project, to view it start the Django development webserver and open your browser to [localhost:8000](http://localhost:8000).

```bash
python manage.py runserver
```

### Coming back to the project
If you've already installed the dependencies you can activate the virtual environment to jump back in to where you left off.

```console
source .virt/bin/activate
```

### Loading data for the exercises
Data has been saved to seed the data base for various parts of the class, to load these you'll want to use the django `loaddata` command.

```console
python manage.py loaddata exercise-1.json
```

You'll want to **drop, create, and migrate** your data base before loading data if you wish to start with a fresh DB.

```console
dropdb orms
createdb orms
python manage.py migrate
python manage.py loaddata exercise-1.json
```

From the shell, you should now have a data base populated with sample data.

```console
python manage.py shell_plus

In [1]: User.objects.all()
Out[1]: [<User: Lenard Dilucca>, <User: Carylon Ryant>, <User: Keira Diseth>]

In [2]: Ship.objects.all()
Out[2]: [<Ship: USS Enterprise>]

In [3]: Log.objects.all()
Out[3]: [<Log: USS Enterprise - Keira Diseth - Stardate 69683, all is well aboard the Enterprise>]
```

## License
The MIT License (MIT)
