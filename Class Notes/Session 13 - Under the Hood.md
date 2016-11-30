# Regex

## Structure of a Regex

Most characters in a regex are matched literally.  In addition, the default behavior of regex matching is to look for the pattern anyplace in the string.  For example, 'low' would match 'helloworld' starting at character 4.

There are also character classes that match any 1 character from the class.  Examples include ```[a-zA-Z] and [abcd1234]```.

You can negate character classes (matching any character that is not in the character class) by starting them with a caret.  ```'[^a-z]' and '[^,]'```

There are also special character classes.  ```'\d' and '[:digits:]', '.'```

\\ is the escape character, though some special characters lose their meaning inside of brackets.

It's possible to specify repetition.  ```'h+', '[a-z]*', '\d?', and '\s{0,5}'```

Pattern{min, max} means from min to max occurrences of the preceding pattern.  If max is blank, that means no limit.  + is {1, }, * is {0, }, and ? is {0,1}.

In addition it's possible to group things together with parentheses.  ```'(ba)+' and '([0-9]\+)*'```

It's also possible to interrogate context with lookarounds.  ```'this text will be matched(?= and this has to be there, but will not be matched)', '\bword boundary\b', 'end of string$', '^start of string'.```

In addition, it's possible to refer to previous matches.  ```'(match me twice in a row)\1', '(\w+)\1'```

Last, it's possible to have alternatives.  ```'(this)|(that)'```

There's more, but this is enough to do lots.  Here are some example regex expressions:
- ```'\d{3}([-\. ])\d{3}\1\d{4}'``` matches '503-123-1234' or '503.123.1234', but not '503-123.1234'.
- ```'<[^>]*>'``` matches '<span>' and '< a href="http://http.cat/">'.
- ```'#?([\da-fA-F]{2})+'``` matches '#ae1246' and 'EE45'

Two additional notes that we won't get into tonight:

1. It's often efficient to have the computer build a regular expression for you.  This can allow you to have expressions that are more complicated (read powerful) than you would want to maintain by hand).
2. You can add comments to regular expressions if you end up having to do something really funky (comments are a little hard to work with, so I don't encourage them here as much as I do most of the time.).

## Regex Functions in Postgres

~ is a beefier version of LIKE and takes regexes.

```sql
SELECT *
FROM crimedata.crimedataraw
WHERE neighborhood ~ '\w+\s+\w+' --two word neighborhood

```

SUBSTRING returns the first match group, if it can find one, otherwise the first match.

```sql
SELECT SUBSTRING('phone 503-733-1221' from '\d{3}([-\. ])\d{3}\1\d{4}') AS whole_number,
	SUBSTRING('phone 503-733-1221' from '\d+') AS area_code,
	SUBSTRING('phone 503-733-1221' from '\d+-(\d+)') AS exchange
```

REGEXP_REPLACE let's you do string manipulation.

```sql
SELECT REGEXP_REPLACE('phone 503-733-1221', 'phone\s*', 'ph:'),
    REGEXP_REPLACE('phone 503-733-1221', '-', '.', 'g'),
    REGEXP_REPLACE('phone 503-733-1221', '.*(\d{3})[^\d]*(\d{3})[^\d]*(\d{4}).*', '(\1)\2-\3')
```

It's also possible to simply pull out the matching values with REGEXP_MATCHES

```sql
SELECT REGEXP_MATCHES('one, two, three, four, five', '\w+', 'g')
```

## Other Uses of Regex

Regular expression are fairly common, especially in the unix world.  A common command that uses them is grep.  If you haven't used this command before, it's worth learning.  It is like cat, except that it only display rows that match a given regular expression.

```bash
grep 'powell' buildCrimeDataRaw.sql
```



# Postgres Under the Hood

## Indexes

Postgres indexes store sorted data and ctid (physical address)

### BTree

Generalized binary tree (not actually binary).  These are balanced trees that have many children (to optimize disk access).

### RTree

Find the containing rectangle for all spacial elements and then group them based on those rectangles.  Each level up in the tree stores the containing rectangle of the composite of it's children's rectangles.

### GiST-Generalized Search Tree

The library that was used to implement RTrees in Postgres.


## Joins

### Loop Join

For each row in the first table, lookup each related row in the second table.  These can be O(n*m) or faster, depending on whether the second lookup requires a table scan or not.  O(1) memory requirements.

### Hash Join

Put the first row into a hash array.  Hash the second table into the same hash array.  This is linear time, but requires enough memory to store the entirety of the smallest table in working memory. O(n+m) time, but O(n) memory requirements.  It also only works if the join criteria hold true after hashing the input (shorthand is that it only works when equals is the operator).

### Merge Join

Ensure the tables are sorted.  Start with the lowest element in each table and move up one element in whichever table was lowest.  O(n+m) time.  O(1) memory requirements.

## System Optimizations

### Query Optimizer

Rewrite queries as needed.  Determine best procedural steps to get to results.  For instance, if you have the following query, the system might choose to test ID first and it might choose to test password first.  If you have typical indexes, looking up ID first will be far faster.

```sql
SELECT 1
FROM users
WHERE ID = 'alice'
	AND password = 'password';
```

#### Immutable Functions

The system tracks whether a function is allowed to change results between calls.  It's incapable of determining that for python functions.  If the results never change, the function will only be called once.

#### Stats

The system tracks basic statistics on the values of each column.  It can use this info to guess about which criterion will be most helpful in getting to the answer.

### Caching

Take guesses about what data will be used regularly.  The algorithms employed are fairly good.

## Explain Plan

What the system is actually doing and how much it costs.  Virtually every query tool has a button to see the execution plan.

## CTID/Vacuum

The ctid is the physical location of a record on disk.  It can change.  When a record is updated, a new copy of the record is made with a different ctid and version number.  When a query looks at a table, it only looks at versions that were created when the query started.  If a new version is created after a query is started, that version is ignored.  It's impossible to access a version of a row that was not current when you started your query.  The VACUUM command clears out inaccessible rows and frees up the space.  It can be set to run by default.  


## Tasks

1. Create a table called Words with all 26^5 5-character words and the structure:  ID, word
2. Pull back * where word = 'me%' using in, like, regex, and left.
3. Create an index on word and re-execute the queries from 1b.  What happed to the execution time and plan?

4. Create a query to return 10 words, their IDs and the IDs of the reverse of those words (e.g., the ID of 'abcde' and 'edcba').  Look at the execution plan and time.
5. Drop the index and reexamine the results.

6. Create a regex to match regular email addresses.  Test it.

7. Create a regex to match all words from Words that only contain vowels.  
8. Create a regex to match all words from Words that contain exactly two vowels.

9. Replace multiple spaces in a sentence with a single one using a regex replace (e.g., fix the spacing on 'This  sentence   has too much     whitespace.').

10. Make an acronym from a sentence using a regex (e.g., 'Light Amplification-by Stimulated Emission-of Radiation' -> 'LASER').

11. Make a regex that matches 6 character palindromes (e.g., 'abccba' but not 'abcdcb').
