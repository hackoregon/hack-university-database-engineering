# Normalization

## Union
You can stack query results vertically with the union keyword.  The columns of the combined set will match the schema of the first set in the union and you will get an error if the second set doesn't match that schema.  

```SQL
SELECT 1
UNION
SELECT 2
UNION
SELECT 2
```

Union automatically behaves as if a distinct keyword was added to the query.  This behavior can be turned off by saying union all.

```SQL
SELECT 1
UNION ALL
SELECT 2
UNION ALL
SELECT 2
```

There are equivalent commands for intersection and exclusions (intersect and except).  I don't use them because the way they determine matches isn't intuitive to me.

## Domains
Columns/variables can only hold certain values.  That set of values is the domain of the variable.  The data type of the column defines the basic set of values that's acceptable.  Constraints can further reduce the domain of the variable.

### Constraints

#### Column Constraints

```SQL
CREATE TABLE schema.table
(
	col1 Datatype column_constraint
)

column_constraint:
[NOT] NULL
CHECK (test_involving_this_column)
UNIQUE
PRIMARY KEY
REFERENCES other_table (col1, col2)
```

#### Table Constraints

All of the column constraints (except not null) have equivalent table constraints.

```SQL
CREATE TABLE schema.table
(#### Table Constraints
All of the column constraints (except not null) have equivalent table constraints.
	col1 Datatype,
	table_constraint
)
table_constraint:
[CONSTRAINT name] the_rest

the_rest:
CHECK (test_involving_any_columns)
UNIQUE (local_col1, local_col2, ...)
PRIMARY KEY (local_col1, local_col2, ...)
FOREIGN KEY (local_col1, local_col2, ...) REFERENCES other_table (foreign_col1, foreign_col2, ...)
```

## Indexes

The database will automatically maintain sorted copies of part of your data allowing optimization of certain operations.

```SQL
CREATE [UNIQUE] INDEX index_name ON table_name (col1, col2);
```

## ERD

### Chen Diagrams

Chen diagram is a rectangular entity with elliptical attributes attached to it.  Diamonds describe relationships.  Double lines to attributes mean multi-valued (i.e., your design work isn't done there yet). Dashed line indicates a derived attribute.  Relationship cardinality is expressed as '(min, max)' on the 2 lines coming out of the relation.

### Crow Foot Diagrams

Crow foot diagram has rectangle for each entity.  The rectangle is divided into two columns, the left having pk/fk tags and the right listing attributes.  It's also divided top and bottom where pk attributes appear above a line and other attributes below.  Relationships are expressed as lines between entities that have icons on the end: crows foot to say that multiple records in this entity appear in this relationship (no crows foot implies that it's never more than 1), two vertical bars for required, circle for optional (will be paired with crows foot), single vertical bar for required (will be paired with crows foot).

### UML

UML (Unified Modeling Language)
Similar to crow foot except that only attribute names are listed in the entities and there are no crows feet.  Cardinality is expressed with 'min..max' on each end of a relationship.
assignments

## Normalization

### Dependency

- Knowing field A means that you automatically know field B.  E.g., zip_code->City
- The concept of dependency is used in both 2nd and 3rd normal forms.

### 1st Normal Form 1NF

- No ordering for rows
- No ordering for columns
- No duplicate rows
- Each "cell" only holds 1 value (neighborhood doesn't hold two distinct values)
- Has a primary key

### 2NF - not discussed often

- 1NF
- If there is a composite candidate key (unique minimal key), it isn't possible to predict the value of any column if you know part of the candidate key (e.g., dependents->employee_id, dependent_id, name, employee_salary; employee_id, dependent_id would be a candidate key and employee_salary could be determined from employee_id alone.)

### 3NF

- 2NF
- There aren't any non-key columns that allow you to predict other non-key columns with perfect accuracy (e.g., crime_data->id, neighborhood, xcoord, ycoord).


### Denormalization

- Normal forms are great, but the most important thing is that the system works for your needs.
- Reporting systems typically have different requirements than transactional systems.

### Dimensionality Analysis (star schema)

Dimensions (string or time values typically) are extracted into dimension tables.  A fact table has numeric data and links to dimension tables (e.g., region, product, date, and sales_person are dimensions.  Items_sold and total_value_sold are facts).



TASKS

1. Run the first two queries.

```SQL
SELECT neighborhood
INTO TEMP t
FROM crimedataraw
GROUP BY neighborhood

SELECT neighborhood
INTO TEMP t2
FROM crimedataraw
WHERE major_offense_type = 'Runaway'
GROUP BY neighborhood
```

Next, rewrite this query without using any inner or outer joins.

```SQL
SELECT *
FROM t LEFT OUTER JOIN t2
	ON t.neighborhood = t2.neighborhood
```

2. Select the crime types and counts into a temp table.  Select 1 record from this table and then delete that record.  Make sure that your select/delete queries will work the second and third time they're executed.  How do you know that you deleted the correct record?

3. Create a CTE to join crimedataraw and the two related tables.  Select all of the data from it.  How long did it take?  Run it several times and right down how long it takes.

4. Create primary key constraints on all appropriate columns for 3 crime data tables.

5. Create foreign key constraints on all appropriate columns for crime data tables.

6. How long does the CTE query take now?

7. Create a timestamp column that combines the time and date.  Call it report_time_date.

8. Use a correlated subquery to select all of the information on each crime plus the crime type of the previous crime committed in the same neighborhood.  Do not use a windowing function here.  How long does the query take.  Execute it several times and write down how long it takes.

9. Add an index for that subquery.  How long does the query take now?

10. Create a new varchar column called test_column on crimedataraw.  Run an update statement to assign the value 'value' to the test column for every row.  Write down how long it took.  Run the update several times.  Write down the execution time for each run.  Create 3 new indexes on crimedataraw that include the column test_column.  How long does the update take now?

11. Draw an ERD for our crime data.  What would you change to make it 3rd normal form?  Do it.  What would you change to make it more useful for our queries?
