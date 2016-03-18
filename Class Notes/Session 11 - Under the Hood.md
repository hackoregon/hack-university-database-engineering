##Regex
###Structure of a Regex
Most characters in a regex are matched literally.  In addition, the default behavior of regex matching is to look for the pattern anyplace in the string.  For example, 'low' would match 'helloworld' starting at character 4.

There are also character classes that match any 1 character from the class.  Examples include '[a-zA-Z]', '[abcd1234]', 

You can negate character classes (matching any character that is not in the character class) by starting them with a caret.  '[^a-z]', '[^,]'

There are also special character classes.  '\d', '[:digits:]', '.'

\ is the escape character, though some special characters lose their meaning inside of brackets. 

It's possible to specify reptition.  'h+', '[a-z]*', '\d?', '\s{0,5}'

In addition it's possible to group things together with parentheses.  '(ba)+', '([0-9]\+)*'

It's also possible to interogate context with lookarounds.  '(?=this has to be there, but will not be matched)', '\bword boundary\b', 'end of string$', '^start of string'.

In addition, it's possible to refer to previous matches.  '(match me)\1', '(\w+)\1'

Last, it's possible to have alternatives.  '(this)|(that)'

There's more, but this is enough to do lots.  Here are some example regex expressions.
'\d{3}([-\. ])\d{3}\1\d{4}' matches '503-123-1234' or '925.240.1275', but not '503-123.1234'
'<[^>]*>' matches '<span>' and '<a href="http://http.cat/">'
'#?([\da-fA-F]{2})+' matches '#ae1246' and 'EE45'

###Regex Functions in Postgres
~ is a beefier version of LIKE and takes regexes. 

```SQL
SELECT *
FROM crimedataraw
WHERE neighborhood ~ '\w+\s+\w+' --two word neighborhood
```

SUBSTRING looks for the first match group, if it can find one, then the first match.
```SQL
SELECT SUBSTRING('phone 503-733-1221' from '(\d{3}([-\. ])\d{3}\1\d{4})') AS whole_number,
	SUBSTRING('phone 503-733-1221' from '\d+') AS area_code,
	SUBSTRING('phone 503-733-1221' from '\d+-(\d+)') AS exchange
```

REGEXP_REPLACE let's you do string manipulation.
```SQL
SELECT REGEXP_REPLACE('phone 503-733-1221', 'phone\s*', 'ph:'),
    REGEXP_REPLACE('phone 503-733-1221', '-', '.', 'g'),
    REGEXP_REPLACE('phone 503-733-1221', '.*(\d{3})[^\d]*(\d{3})[^\d]*(\d{4}).*', '(\1)\2-\3')
```

It's also possible to simply pull out the matching values with REGEXP_MATCHES
```SQL
SELECT REGEXP_MATCHES('one, two, three, four, five', '\w+', 'g')
```

###other uses of regex 
Regular expression are fairly common, especially in the unix world.  A common command that uses them is grep.  If you haven't used this command before, it's worth learning.

```bash
grep 'powell' buildCrimeDataRaw.sql
```



##Postgres Under the Hood
###Indexes
Postgres indexes store sorted data and ctid (physical address)
####BTree
Generalized binary tree.
####RTree
Cluster elements and define the containing rectangles
####GiST-Generalized Search Tree
The library that was used ot implement RTrees in Postgres


###Joins
####loop join
for each row in the first table, lookup each related row in the second table
####hash join
put the first row into a hash array.  Hash the second table into the same hash array.
####merge join
ensure the tables are sorted.

###System Optimizations
####Query Optimizer
Rewrite queries as needed.  Determine best procedural steps to get to results
#####immutable functions
Can the function be pushed up or not?
#####stats
####Caching
Take guesses about what data will be used regularly

###Explain plan
What the system is actually doing and how much it costs.


##Tasks
1a.Create a table called Words with all 26^3 3-character words and the structure:  ID, word
1b.Pull back * where word = 'me%' using in, like, regex, and left.
1c.Create an index on word and re-execute the queries from 1b.  What happed to the execution time and plan?

2a.Create a correlated nested subquery on Words.  Look at the execution plan and time.
2b.Drop the query and reexamine the results.

3.Create a regex to match email addresses.

4.Create a regex to match all words from Words that only contain vowels.  That contain exactly two vowels.

5.Replace multiple spaces in a sentence with a single word using a regex replace.

6.Make an acronym from a sentence using a regex.

7.Make a regex that matches 6 character palindromes.