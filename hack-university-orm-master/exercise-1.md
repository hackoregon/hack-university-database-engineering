# Exercise 1 - getting setup

## Part 1 - set up your Django project

Follow the instructions in the [README.md](README.md#quick-start) Quick start to get your project up to speed. Check with the instructor before continuing.

## Part 2 - load existing data

Django has a built-in management command to dump and load data. From the `orms` project run the `loaddata` to populate the data base. You will need to be in the `orms` project which has the file `manage.py` in its directory.


    python manage.py loaddata exercise-1.json


You should see the output

    Installed 10078 object(s) from 1 fixture(s)

## Part 3 - gain access to the Django shell (shell_plus)

`django-extensions` should be installed into your virtualenv. This can be verified by the command `pip list`.

Open the shell up to access the Django ORM. 

```console
python manage.py shell_plus
```

## Part 4 - query all the ships in the data base

If you used `shell_plus` to enter the shell you likely have an `iPython` shell and registered Django app modules pre-loaded.

If you don't, you'll need to import the python module representing the ORM model of a ship.

```py
In [1]: from logs.models import Ship

In [2]: queryset = Ship.objects.all()

In [3]: print(queryset)
[<Ship: USS Enterprise>, <Ship: USS Voyager>, <Ship: USS Orion>, <Ship: USS Luna>, <Ship: USS Ares>]

In [4]: print(queryset.query)
SELECT "logs_ship"."id", "logs_ship"."name", "logs_ship"."capacity" FROM "logs_ship"

```
