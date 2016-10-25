# Other Queries

## Distinct
You can put the keyword DISTINCT next to select in a query and it will achieve the same result as adding a group by clause and listing all of the columns in your select list there.

## More on Aggregate Functions
COUNT(col), COUNT(\*), COUNT(DISTINCT col), COUNT(\*) FILTER (WHERE col2 = 5)

## Window Functions
COUNT(\*) OVER (PARTITION BY neighborhood) other functions defined at
http://www.postgresql.org/docs/current/static/functions-window.html#FUNCTIONS-WINDOW-TABLE

## Joins

### Join Types
The default join type is a cross join, which takes all possible combinations of records from both tables (the cartesian product).  Most joins let you break apart the where clause to show which parts are logically related to the join (the on clause) and which are regular filters (the where clause).  For inner joins, the on clause behaves identically to the where clause.  For left outer joins, if a record in the table on the left doesn't ever get a true value for the on clause, the record is included without a table on the right.

### Join Syntax
```
FROM t1 AS l INNER/LEFT/RIGHT/FULL JOIN t2 r
	ON l.col = r.col
```
```
FROM t1 AS l CROSS JOIN t2 r
```
## Subqueries

### Table Expression Subqueries
```
SELECT *
FROM (SELECT ID, neighborhood FROM crimedata.crimedataraw) alias_for_subquery;
```

### List Subqueries
```
SELECT *
FROM crimedata.crimedataraw
WHERE neighborhood IN (SELECT neighborhood FROM crimedata.crimedataraw WHERE major_offense_type = 'Runaway');
```

### Scalar Subqueries
```
SELECT *
FROM crimedata.crimedataraw o
WHERE o.neighborhood = (SELECT neighborhood
			FROM crimedata.crimedataraw
			GROUP BY Neighborhood
			ORDER BY COUNT(*) DESC
			LIMIT 1)
LIMIT 100;
```


### Correlated Subqueries
```
SELECT neighborhood
FROM crimedata.crimedataraw o
WHERE EXISTS (SELECT 1 FROM crimedata.crimedataraw i
							WHERE i.neighborhood = o.neighborhood AND i.major_offense_type = 'Runaway')
GROUP BY neighborhood;
```
```
SELECT neighborhood, CASE WHEN (	SELECT 1
					FROM crimedata.crimedataraw i
					WHERE i.neighborhood = o.neighborhood AND i.major_offense_type = 'Runaway'
					LIMIT 1) IS NOT NULL THEN 'has' ELSE 'doesn''t have' END || ' runaway'
FROM crimedata.crimedataraw o
GROUP BY neighborhood;
```

### Common Table Expressions (CTE)
```
WITH alias_for_subquery AS
(
	SELECT * FROM crimedata.crimedataraw
)
SELECT *
FROM alias_for_subquery;
```


## Create Table
```
CREATE TABLE schema.name
(
	col1 type,
	col2 type,
	col3 type
);
```

### Temp Tables
These tables only exist for the duration of your session.
```
CREATE TEMP TABLE name
(
	col1 type,
	col2 type,
	col3 type
);
```

## Alter Table
```
ALTER TABLE TABLE ADD col1 type;
```

## Insert into
Another way to create a table is through an insert into clause on a select statement.
```
SELECT col1
INTO TABLE2
FROM TABLE1;
```
## Update
Update statements modify existing data in a table.
```
UPDATE TABLE SET col1 = val
FROM other_TABLE --this clause is optional
WHERE join_criteria; --this clause is optional
```

## Insert
Insert queries insert new data into an existing table.
```
INSERT INTO schema.table (col1)
VALUES (1),
	(2),
	(3);
```
```
INSERT INTO schema.table (col1)
SELECT col10
FROM schema.table2;
```

## Delete
Delete queries remove data from a table.
```
DELETE FROM schema.table
WHERE neighborhood = 'Brooklyn';
```

## Drop
Drop queries remove an existing table.  All the data that was in that table gets erased when you drop a table.
```
DROP TABLE schema.table;
```


## Assignment

1. For each crime type, count the number of neighborhoods where it happened.

2. Create sentences for the different crime types saying "<crime type> isn't ok."

3. Extract distinct crime types from crimedataraw using SELECT INTO and then add an id column.  Name the table crime_types.

4. Add appropriate crime type id to crimedataraw.

5. Repeat for neighborhood names using CREATE TABLE and not altering the table after.  Name the table neighborhoods.

6. Pull back the number of each crime type committed per neighborhood (0 if there were 0).

7. Assuming that each neighborhood is square and lines up with the coordinate system, which neighborhood has the highest crime rate per square foot?  Can you do it with one query?

### Harder Questions

1. Which neighborhood has the highest rate of each type of crime?  Can you do it with one query?

2. List each crime and show the type of the previous crime committed in that same neighborhood.  

3. Modify crime type table to include cost_per_crime and populate with data similar to what's found at http://www.rand.org/jie/justice-policy/centers/quality-policingg/cost-of-crime.html.  Do the modification by inserting the new values into a temp table and then doing a join to allow a batch update to the major crime table.

4. Pull back total crimes and total crime cost for each neighborhood.

5. Which crime has the highest total cost by for each neighborhood.
