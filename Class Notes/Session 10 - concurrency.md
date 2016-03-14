##PLPGSQL
Not called directly from prompt.  DO statement lets you use it.

```SQL
DO $$
DECLARE
	myvar integer;
BEGIN
	UPDATE neighborhoods SET ID = ID;
END;
$$;
```

There are a fair number of limitations.  You can't return results from select using DO. SELECT INTO doesn't work like it does for SQL.  You can return results when using PLPGSQL in a function.

Otherwise, it's quite similar to SQL with the addition of variables and control structures.


##Transactions

Transactions group work and make sets of instructions atomic.  All instructions are either commited or abandoned as a set.
```SQL

BEGIN;
SELECT 5 AS i INTO t;
COMMIT;
BEGIN;
UPDATE t SET i = 15;
ROLLBACK;
SELECT * FROM t;
```
The related commands are:
BEGIN  <- often implicit
ROLLBACK
COMMIT <- often implicit

Postgres incorporates DB snapshots at the most basic level.  
In one window run this:
```SQL
BEGIN;
UPDATE t SET i = 15;
```

then run this in another window:
```SQL
SELECT * FROM t;
```

In the first window, run this:
```SQL
COMMIT;
```
Now rerun the command in the second window.

Reads and writes don't block each other, but writes do block each other.

Now, close all your query windows and open two new ones.  In the first window, run this:
```SQL
UPDATE t SET i = 0;

BEGIN;
UPDATE t SET i = 15;
```

Run this in the second window:
```SQL
BEGIN;
UPDATE t SET i = 15;

DO $$
DECLARE
	local_i integer;
BEGIN
	 local_i = (SELECT i FROM t);

	UPDATE t set i = local_i + 5;
END;
$$;
```

Last, run this in the first window:
```SQL
COMMIT
```

What value does t hold?

These locks happen at the row level.

This is READ COMMITED.  You can up the ante to REPEATABLE READ, which would prevent the update the in the example above and return an error.

REPEATABLE READ would still have let the update happen if the rows weren't the same though, so you could have an example like this.

myt
class, frequency
1, 1
2, 1

```SQL
INSERT INTO myt SELECT 1, SUM(frequency) FROM myt WHERE class = 2
```
```SQL
INSERT INTO myt SELECT 2, SUM(frequency) FROM myt WHERE class = 1
```

Both statements would affect the output of the other.  You can prevent issues like this by using SERIALIZABLE 

I rarely escalate my locking level and you probably don't usually need to either.  Some systems use locks to ensure that you have adequate.  Postgres prefers Multiversion Concurrency Control (MVCC).  Basically, any time you update a record, postgres makes a new copy of that record.  It has a complicated system to ensure that every query knows which version of a record to read.

That means that updates, leave both copies.  There are a few other things that can leave extra copies of rows in a table.  VACUUM is the command that goes through and sweeps up the old copies.


##Error Handling
Uncaught errors cause abortion of transaction.  They can be caught with an EXCEPTION clause in your code block.

DECLARE
BEGIN
EXCEPTION
END;

Once they're caught, you can 
SQLSTATE contains error code
SQLERRM gives the error description
```SQL
GET CURRENT DIAGNOSTICS
GET STACKED DIAGNOSTICS text_var1 = MESSAGE_TEXT,
                          text_var2 = PG_EXCEPTION_DETAIL,
                          text_var3 = PG_EXCEPTION_HINT;
```
Those commands get the current state and the state as of the last exception, respectively.

You can raise you own errors.  
```SQL
RAISE EXCEPTION '%', variable
```
There are other levels of events that you can raise: DEBUG, LOG, INFO, NOTICE, and WARNING

###Security
Based on roles.  Roles can act as user or group or both.  We've been using super users, which ignore these rules.

Control access to DB
-Account based controls
-Connection based controls
-Limited tools to enforce good password management

Control what can be done in the DB
-lock objects
-lock columns
-row level security

Privilege escalation
-SQL Injection (http://xkcd.com/327/)
-Insecure architecture

Confidential data
-PII
-Standard restrictions (HIPAA, FISMA, PCI)
-Contract specific restrictions

Inadvertent Release
-It's often possible to fill in details with data that you provide.
-example 1: website for class action lawsuit that accepts name and address and says if the user is in the class or not.  What if the class is people who've had side effects from medication to treat paraphilia?
-example 2: AOL search data.  https://en.wikipedia.org/wiki/AOL_search_data_leak
