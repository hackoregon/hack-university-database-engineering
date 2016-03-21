# Object-Relational Mapping (ORM)

## Overview

ORMs provide idiomatic access to data in data bases. In Python, this means data base rows are translated into Python objects and relations are represented commonly as attributes or methods. Queries can be represented as Python objects, and querying the database is often lazily evaluated, allowing the programmer to create queries as and pass them through the program to be updated and evaluated only when needed.

## Motivation 

#### the old way
```python
import MySQLdb
import config

connection = MySQLdb.connect(
    host=config.HOST,
    user=config.USER,
    passwd=config.PASS,
    db='test'
)
cursor = connection.cursor()
sql = """SELECT foo id FROM foo WHERE bar IN ('A', 'C')"""
cursor.execute(sql, args)
data = cursor.fetchall()
print(data)
```

#### with an ORM
```python
data = Foo.objects.filter(bar__in=['A', 'C'])
print(data)
```

Connecting to the database via the shell may feel very natural when needing to run a report, adjust some data, or batch process a new set of data, but using raw SQL statements within a program has its limitations and security concerns, and wouldn't it be far easier to use python to interact with the database from a python program?

## Advantages

The Django ORM was once described to me as providing the means to scale developers, especially developers without strong DB knowledge.  I don't think this is entirely true, but, without knowing SQL or how a relational database is created or typed, someone using Django can write, request.user.first_name and have the string first name of the web user without having to know a database was involved. 

1:1 parity between DB rows and Python objects  
Pooling and open connections  
Idiomatic Error handling  
Multiple databases  

## Disadvantages

Constraints on modeling data (see SQLAlchemy vs. Django-ORM), what if an object is represented over multiple tables or a row in a table should represent multiple Python objects?   
Bad queries: n+1  
Deep knowledge in making good queries: select-related, prefetch-related  
Configuration of DB is needed (though standard)  
SQL is not translated 1:1 to the ORM DSL  
New ideas like QuerySet  
JSONB anyone  

## CYOA

Most ORMS allow the use of raw sql when desired. Normally, this is to fulfill one of two conditions: there's a complex query or unique query or stored procedure that the ORM cannot form or the ORM is getting in way and mangling a simple query. 

```pycon
In [33]: for c in Crimedataraw.objects.raw('SELECT * FROM crimedataraw'):
    print(c.__dict__)
    break
   ....:
{'_state': <django.db.models.base.ModelState at 0x10a2a3f10>,
 'address': u'Unknown/Not Available',
 'id': 10,
 'majoroffensetype': u'Sex Offenses',
 'neighborhood': u'SOUTH PORTLAND',
 'policedistrict': u'890',
 'policeprecinct': u'PORTLAND PREC CE',
 'recordid': 14282253,
 'reportdate': datetime.date(2014, 1, 6),
 'reporttime': datetime.time(9, 25),
 'xcoordinate': None,
 'ycoordinate': None}
```

## The Django ORM

Django provides a default ORM with their framework, other popular python ORMs are [SQLAlchemy](http://www.sqlalchemy.org/) and [records](https://pypi.python.org/pypi/records/).

While it's possible to use the Django ORM without a Django project and app, some scaffolding is needed to satisfy its expected structure. See [Introspection](#introspection).

### Modeling Data

>A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

#### A sample model of a star ship

```py
class Ship(models.Model):
    """A starship."""

    name = models.CharField(max_length=128, unique=True)
    capacity = models.IntegerField(
        blank=True, null=True, help_text='Max number of passengers'
    )
    passengers = models.ManyToManyField(User, blank=True, related_name='ships')

    def __unicode__(self):
        """The string and unicode representation."""
        return u'{self.name}'.format(self=self)
```

### Querying Data

### Basics (99% of your time with Django-ORM)

- CRUD
- Filtering and Excluding
- Joins
- Migrations
- .all, .none, .count, .first, .last
- Update (prevent race conditions) and Delete

### Intermediate

- Aggregations: AVG, MAX, MIN, SUM
- Group By: COUNT
- Bulk create

### Advanced

- Select related & prefetch related
- Q
- F
- Extending Query and QuerySet
- .raw and .extra
- connection queries & cache (profiling and debugging)




## Introspection 
What if a data base already exists and it was not created nor managed using the ORM
you have at hand?

Most ORMs provide a way to integrate with an existing data base, whether to migrate to a new application code base, to normalize over several different data base syntaxes (MySQL, PostgreSQL, Oracle, MS SQL, etc.), or because a developer is more familiar with a particular ORM. Django provides the management command [`inspectdb`](https://docs.djangoproject.com/en/1.9/howto/legacy-databases/)  

```console
python manage.py inspectdb > models.py
```

Then we can inspect that data via the Django ORM.  

```pycon
In [13]: qs = Crimedataraw.objects.values('neighborhood').annotate(n_count=Count('neighborhood'))

In [14]: print(qs.query)
SELECT "crimedataraw"."Neighborhood", COUNT("crimedataraw"."Neighborhood") AS "n_count" FROM "crimedataraw" GROUP BY "crimedataraw"."Neighborhood"

In [15]: {d['neighborhood']: d['n_count'] for d in qs[:10]}
Out[15]:
{u'BRIDGETON': 73,
 u'CULLY': 1149,
 u'GRESHAM - NORTH CENTRAL': 3,
 u'GRESHAM - NORTH GRESHAM': 6,
 u'HOSFRD-ABRNETHY': 878,
 u'MILL PARK': 817,
 u'ROSE CITY PARK': 357,
 u'UNIVERSITY PARK': 339,
 u'W PORTLAND PARK': 141,
 u'WOODSTOCK': 600}

# And we can order that too
In [21]: {d['neighborhood']: d['n_count'] for d in qs.order_by('-n_count')[:10]}
Out[21]:
{u'CENTENNIAL': 2076,
 u'CHINA/OLD TOWN': 3243,
 u'DOWNTOWN': 5394,
 u'HAZELWOOD': 3727,
 u'LENTS': 2513,
 u'LLOYD': 1542,
 u'MONTAVILLA': 1374,
 u'NORTHWEST': 2047,
 u'PEARL': 1549,
 u'POWELHST-GILBRT': 2437}
```

## Entity-Relationship Diagram (ERD)

A visual representation of the relations can be generated from the Django ORM via the third-party-app `django-extensions`, which provides the Django management command [`graph_models`](http://django-extensions.readthedocs.org/en/latest/graph_models.html). 

The install for `pygraphviz` can be cumbersome and on OSX requires the `graphviz` installed system-wide.

One the python dependency `pip install pygraphviz` is available, an ERD of your app can be made easily.

```pycon
python manage.py graph_models logs --pygraphviz -o orms_erd.png
```

Here's the generated file for the `logs` app.

![orms_erd.png](orms/orms_erd.png)


# Class Q/A

How can we find the fields for a given model?
```py
In [46]: ship = Ship.objects.all()[0]

In [47]: ship.__dict__
Out[47]:
{'_state': <django.db.models.base.ModelState at 0x7f2c3b3e7110>,
 'capacity': 2860,
 'id': 2,
 'name': u'USS Voyager'}

In [48]: vars(ship)
Out[48]:
{'_state': <django.db.models.base.ModelState at 0x7f2c3b3e7110>,
 'capacity': 2860,
 'id': 2,
 'name': u'USS Voyager'}
 ```
