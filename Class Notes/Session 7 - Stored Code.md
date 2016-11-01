# Transactions

## Prep

Open Pgadmin3, go to file-&gt;Options-&gt;Query Tools-&gt;Query Editor and uncheck Enable Auto ROLLBACK.

## The Basics

Transactions group work and make sets of instructions atomic.  All instructions are either committed or abandoned as a set.

```sql

BEGIN;
SELECT 5 AS i INTO TEMP t;
COMMIT;
BEGIN;
UPDATE t SET i = 15;
ROLLBACK;
SELECT * FROM t;
```

The related commands are:

- BEGIN  &lt;- often implicit
- ROLLBACK
- COMMIT &lt;- often implicit

Postgres incorporates DB snapshots at the most basic level.
In one window run this:

```sql

BEGIN;
UPDATE t SET i = 15;
```

then run this in another window:

```sql

SELECT * FROM t;
```

In the first window, run this:

```sql

COMMIT;
```

Now rerun the command in the second window.

Reads and writes don't block each other, but writes do block each other.

Now, close all your query windows and open two new ones.  In the first window, run this:

```sql

UPDATE t SET i = 0;

BEGIN;
UPDATE t SET i = 15;
```

Run this in the second window:

```sql

BEGIN;
UPDATE t SET i = 16;

```

## Isolation Levels

Close out the previous windows and open two new windows.

In Window 1, run:


```sql

DO $$
DECLARE
   local_i INTEGER;
BEGIN
    UPDATE t set i = 16;
    local_i = (SELECT i FROM t);

    PERFORM pg_sleep(30);

   UPDATE t SET i = local_i + 5;
END;
$$ LANGUAGE 'plpgsql';
```

In Window 2:

```sql

UPDATE t SET i = 0;
```

What value does t hold?

These locks happen at the row level.

This is READ COMMITED.  You can up the ante to REPEATABLE READ, which would prevent the update the in the example above and return an error.

REPEATABLE READ would still have let the update happen if the rows weren't the same though, so you could have an example like this.

In window 1
```sql


CREATE TABLE myt
(
    class INT,
    frequency INT
);
INSERT INTO myt
SELECT 1, 1
UNION ALL
SELECT 2, 1;

DO $$
DECLARE
   freq INTEGER;
BEGIN
    freq = (SELECT SUM(frequency) FROM myt WHERE CLASS = 1);

    PERFORM pg_sleep(30);

   INSERT INTO myt
   SELECT 2, freq;
END;
$$ LANGUAGE 'plpgsql';
```

In Window 2

```sql


DO $$
DECLARE
   freq INTEGER;
BEGIN
    freq = (SELECT SUM(frequency) FROM myt WHERE CLASS = 2);

    PERFORM pg_sleep(30);

   INSERT INTO myt
   SELECT 1, freq;
END;
$$ LANGUAGE 'plpgsql';
```

Both statements would affect the output of the other.  You can prevent issues like this by using SERIALIZABLE.

I rarely escalate my locking level and you probably don't usually need to either.  Some systems use locks to ensure that you have adequate.  Postgres prefers Multiversion Concurrency Control (MVCC).  Basically, any time you update a record, postgres makes a new copy of that record.  It has a complicated system to ensure that every query knows which version of a record to read.

That means that updates, leave both copies.  There are a few other things that can leave extra copies of rows in a table.  VACUUM is the command that goes through and sweeps up the old copies.

# Stored Code

## Views

Views are basically permanent CTEs.  They can be really helpful to allow you to design the table structure that you need but allow other developers to access the data as if it had a different table structure.

```sql

CREATE VIEW crimedata.neighborhoods AS
	SELECT neighborhood, COUNT(*) AS number_of_crimes
  FROM crimedata.crimedataraw
	GROUP BY neighborhood;
```


## SQL v PLPGSQL

We've only used SQL in this class so far.  It lets you run individual queries (even complex ones that involve subqueries).  Postgres includes PLPGSQL, which is a superset of SQL and include procedure tools (why it's called Procedural Language Postegres Structured Query Language).

Postgres supports many languages for writing functions and stored procedures.

## PLPGSQL

Not called directly from prompt.  DO statement lets you use it.

```sql

DO $$
DECLARE
	myvar INTEGER;
BEGIN
	UPDATE neighborhoods SET ID = ID;
END;
$$ LANGUAGE 'plpgsql';
```

There are a fair number of limitations.  You can't return results from select using DO. SELECT INTO doesn't work like it does for SQL.  You can return results when using PLPGSQL in a function.

### Flow Control

In addition to variables, PLPGSQL lets you use if statements and various loops.  If you need to touch each row of a table one-at-a-time, this is a good tool.

## Functions and Stored Procedures

On some systems, there is a distinct difference between stored procedures and functions.  Postgres doesn't differentiate and only uses functions.

## Triggers

It's possible to configure functions to be executed automatically after (or instead of) certain events.  For instance, you could setup a function to be called immediately after a table is updated.  If you do so, it becomes impossible to update the table without the function being called, in fact, the triggered function needs to succeed for the original update to succeed.

These types of events are called triggers and are both very powerful and very dangerous.  We probably won't dig deeper in this class.

## Error Handling

Uncaught errors cause abortion of transaction.  They can be caught with an EXCEPTION clause in your code block.

```

DECLARE
BEGIN
EXCEPTION WHEN type THEN
END;
```
```sql

DO $$
DECLARE
	text_var1 VARCHAR;
        text_var2 VARCHAR;
        text_var3 VARCHAR;
BEGIN
	RAISE NOTICE 'hi';
	SELECT *
	FROM crimedata.crimedataraw;
EXCEPTION WHEN Others THEN
	RAISE NOTICE 'ooh.  an exception.  :(';
	RAISE NOTICE '% %', SQLSTATE, SQLERRM;

	GET STACKED DIAGNOSTICS text_var1 = MESSAGE_TEXT,
        text_var2 = PG_EXCEPTION_DETAIL,
        text_var3 = PG_EXCEPTION_HINT;
	RAISE NOTICE '% % %', text_var1, text_var2, text_var3;

	END;
$$ LANGUAGE 'plpgsql';
```

Once an exception is caught, you can access some informational variables:

- SQLSTATE contains error code
- SQLERRM gives the error description

In many cases, you'll be able to anticipate what type of errors to except.  In these cases, you should list the specific exception instead of saying, "when others".

You can raise you own errors.

```sql

RAISE EXCEPTION '%', variable
```

There are other levels of events that you can raise: DEBUG, LOG, INFO, NOTICE, and WARNING.  Notice events are the closest thing to console.log functionality.

## Errors inside of Transactions

Run each of these commands one-at-a-time:

```sql

BEGIN;
SELECT 5 AS i
INTO TEMP t;

UPDATE t SET i = 1/0;

SELECT * FROM t;

ROLLBACK;
```

Errors inside of a transaction cause the entire transaction to fail.  This behavior changes by DB.

# Vagrant destroy

To clear out a vagrant box, the command is ```vagrant destroy```.  We'll be using this command regularly over the next few lessons.
