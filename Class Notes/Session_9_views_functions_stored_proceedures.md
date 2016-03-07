# Views, Functions, Stored Procedures, Oh My!

## Overview

These three feature sets are perhaps some of the most abstract that 
relational databases support. Because of this they are both powerful
and relatively complex.

### What do these functions have in common?

Or, why do I need these when I have data in tables and aggregation functions?

Well, these systems are all particularly useful for the *synthesis* of data, not
just writing, querying and grouping data.

For example, various problems require that you keep a running tally of some number
of data points as they go by. Perhaps the number is so large that it is impractical
to store each data point in its own row. Views, Functions and Stored Procedures
offer different ways to massage and normalize this data without undue load
on the storage systems of the database.

These systems take incoming data, apply some logic and transform the data.

### When are they useful?

Like mentioned above, these are useful when we want to keep our data processing
close to the data itself, either for speed purposes, or just for separation
of concerns.

In part, it's a question of fashion. It used to be quite popular to keep
database logic with the data. But because it's not a widely solved problem
for dealing with revisions and updates to that logic, they've somewhat fallen
out of favor.

## Views

Views by themselves are really much like an extension of CTEs(Common Table Expression) covered before.
You can assign a query to a symbol and query from it as if it were a sub select.

This is useful when you have lots of variant queries that all share a base set of data.
You don't want to have to write out the same CTE over and over again.

There is a version of these Views called a Materialized View which instead of just acting as
a short hand for a CTE, it actually physically stores the results (like a cache). Logic
for refreshing this View is configurable.

### Sample View

```PSQL


```


## Functions

SQL is a language! It's easy to forget that it's not just an easy way of describing
how to store data and query it -- but it's a language that's Turing complete -- capable of anything.

Here's how to create a simple function

```PSQL


```

### Notice the type information for the return and the arguments


### What happens if we have two functions with the same name?


### How can we see which functions are loaded?


### How do we update functions?


## Stored Procedures

But RDBMS, and Postgres in particular are not limited to function in SQL. They're able to run 
many other programming languages inside your database!

Since we're all using Python, let's have an example doing that.

### Python


Here's a really simple Python stored procedure:

```python


```


#### Which Libraries Are Available?

This is an important topic, especially considering that one of the major draws of python
is it's expansive and well-used sets of libraries.

It turns out that any library available globally to the python interpreter that 
Postgres is configured to use will be available. So, unlike a lot of applications
which use virtualenvs, you pretty much need to make sure that your system-wide dependencies
are up to date.


### Stored Procedure References

- [PostgreSQL Tutorial.com](http://www.postgresqltutorial.com/postgresql-stored-procedures/)


