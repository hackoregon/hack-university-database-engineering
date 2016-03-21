# Exercise 2 - making queries with the Django ORM

Ref: [https://docs.djangoproject.com/en/1.9/ref/models/querysets/#field-lookups](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#field-lookups)

## Part 1 - counting

Using the Django ORM and the app's Ship and Log models answer the following by using the `count` method:

    Hint: You made need to import the User, Ship, and Log python modules. Ship and Log are available by importing them from logs.models `from logs.models import Log, Ship` but User needs to be imported from Django's standard User model `from django.contrib.auth.models import User`

 - How many ships are there?
 - How many users (crew) exist?
 - How many logs have been made?

## Part 2 - filtering

Using the ORM to filter (`WHERE` clauses) answer the following by using the `filter` method:

- Which ships in the fleet have a capacity over 2,000 passengers?
- Which users have first names ending with 'y'? (hint: `endswith`)

## Part 3 - filtering and counting

Combining both the `filter` and `count` methods, find out how many logs are captain's logs? (`captains_log` is `True`)


## Part 4 - excluding

Using the `exclude` method and the `filter` method, determine which users have first names ending with 'y', but do **not** have last names ending with 'k'? 


## Extra Credit - `in`

Construct a query from the ORM with users have a first name ending with 'y', but do not have the last names 'Centrich' or 'Barick'?
