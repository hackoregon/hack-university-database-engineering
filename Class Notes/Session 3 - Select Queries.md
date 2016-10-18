# Select Queries
## Structured Data
Data that can easily be broken into distinct units is considered structured data.


## Tables
- A collection of records
- Each record has the same structure--the table's schema.
- Important: tables are sets, not lists.  Tables are unordered.

## Naming Conventions
- No spaces in names
- Use lower case and underscores to separate words on PostGRES
- People who work mostly in SQL tend to use plural nouns for table names.  People who mostly work in other languages tend to use singular nouns.  Be consistent and coordinate with the rest of the team.
- Columns should be singular if a given cell holds a single object.
- Tables have underlying name structure of DBName.SchemaName.TableName

## Candidate Keys
- If you have 4 identical rows, how can you ask the database to make a change to one of them?
- A candidate key is a set of columns that don't have any duplicates.
- Typically the database enforces that candidate keys don't have null values or duplicates.

## Schema Example
- Colors: ID, Name, RGB
- Materials: ID, Name, CareInstructions
- Ties: ColorID, MaterialID

## What's a join
- Look at the record for one table.  If it's storing a candidate key for another table, you can also retrieve the corresponding row from the other table.

## NULL
- Two value logic has true and false
- Three value logic can have true, false, and meh (NULL).
- You can't ignore NULLS in your db design. You need to decide what they mean. The most common choice is that NULL means, 'I don't know'.
- If NULL doesn't have a meaning, don't allow NULLs.
- NULL is not the same as an empty string.
- What does 1 + "I don't know" equal?


## Comments
- --comment
- /\*comment\*/

## Basics of Select
### Structure
```
SELECT TOP 10 *
FROM TABLE;
```

### Field Selection
Only pull back certain fields.
```
SELECT TOP 10 field1, field10, field5
FROM TABLE;
```

### Limit
Limit the size of the result set to a certain number of rows.
```
SELECT *
FROM TABLE
LIMIT 10;
```

### WHERE
Only return records where the logical test under where returns true.
```
WHERE 1=0
```
N.B. Think about nulls when you write where criteria.

## Data Types
- smallint
- integer (int)
- bigint
- uuid/guid
- real/float()
- double precision/float()
- decimal(total digits,mantissa digits)
- numeric(total digits,mantissa digits)
- Money
- serial
- varchar()
- char()<-avoid on postgres
- char <-ok on postgres
- text
- bytea
- date
- time
- timestamp
- - w or w/o time zone
- interval
- boolean
- geometric types
- other types

## Aliasing
Aliasing is important in more complicated queries, it lets you assign a limited-scope name to certain entities.
```
SELECT t.id
FROM table t;
```

## Expressions and built in functions
- is null
- Between
- ||
- length
- like
- regex match (~)
- other regex functions
- to_char
- now()
- http://www.postgresql.org/docs/current/static/functions.html
- User-defined functions too

## Order by
The order by clause controls the ordering of the final result set.

## Group by
The group by clause lets you combine records that have identical values in all the listed columns.  Often used to grant access to aggregate functions.

## Having
The having clause is equivalent to the where clause except that it's applied after the group by clause, meaning that you can use aggregate functions in your tests.

## Aggregate functions
- Count
- Min
- Max
- Sum
- Avg

## Assignment
1. Select 5 rows
1. Select date and neighborhood for 10 rows
1. Select the hour of the day for 10 rows
1. Select the second word of the neighborhood name
1. Create a sentence describing what happened on each row for 100 rows (using a query)

### harder problems
1. Select the first row inserted.
1. Select the last row inserted.
1. Select the total crimes by neighborhood.
1. Select the min and max coordinates by neighborhood.  You will use the information to estimate the size of each neighborhood.
1. Which hour has the most crimes?
1. Which day of week has the most crimes?
1. Which season has the highest rate of crime?
