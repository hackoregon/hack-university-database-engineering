##Text Search
###Linguistics
If you remove the inflection from a word, you're left with a lexeme.  By convention, we use the lemma to represent a particular lexeme.  Again by convention, the infinitive of the verb is used as the lemma for verbs.

For example:  ran, run, running, runs, and to run all share the same lexeme and that lexeme is expressed as 'to run' (typically shortened to 'run').  Runner and runnable, however, do not share the same lexeme.

Computational linguistics gets hairy fairy quickly and we won't explore the fact that lead (/lid/) and lead (/lEd/) don't share the same lexeme even though both lexemes would be written as 'lead'.

To enable text searching, postgres has features to allow you to take a string, lemmatize all of the elements, and then produce a sorted list of lemmas.  The documentation refers to these input strings as "documents".

To make search results better, common words are usually stripped from the list during the preparation process.  Every word is looked up in a dictionary (there can be multiple active dictionaries) and only matches are kept.

```SQL
SELECT to_tsvector('english', 'The Fat Rats')
```

Text Search queries can include one or more clauses and the clauses can be combined by & (and) and | (or).  The @@ operator tests a tsvector against a tsquery.

```SQL
SELECT to_tsvector('fat cats ate fat rats') @@ to_tsquery('fat & rat');
```

There are two types of indexes available for tsvectors.
GIN (Generalized Inverted iNdex), each lemma is indexed, with all of it's occurences tracked.

GiST (GeneralIzed Search Tree), all lemmas are hashed into a bit string which is used in OR comparisons.

GIN indexes are usually prefereable.

```SQL
CREATE INDEX ix_quotes_quote_ts_GIN ON quotes USING GIN (quote_ts);
CREATE INDEX ix_quotes_quote_ts_GiST ON quotes USING GIST (quote_ts);
```

In addition to returning matches, postgres will rank the quality of the match for you.

```SQL
SELECT quote, ts_rank(quote_ts, to_tsquery('english', 'dream')) AS rank
FROM quotes
WHERE to_tsquery('english', 'never') @@ quote_ts
ORDER BY rank
LIMIT 10;
```

It's possible to change how the vector preparation is done.  It's also possible to automatically change the query.  For example, you could add a new dictionary to include the word 'hack oregon' as a compound word.  Or, you could put a synonym in for 'colocation' of 'hosting', which would mean that any query for the one would find the other.  For the query modification example, you could substitute  '(cat | dog | horse | mouse | elephant | animal)' for 'animal'.

##NoSQL
NoSQL is a pretty vague term and basically means any database that doesn't try to limit itself to SQL interface.  Examples are column, document, key-value, and graph DBs.

There are two main ingredients in Hadoop.  The cool part is the Hadoop Distributed File System.  The more famous part is map reduce.

###HDFS
HDFS involves chunking up data and distributing it to different child systems.  There will be redundancy and each block of data will be stored on at least one system.  The HDFS can send map reduce queries to each of these systems.  Systems will always try to handle the part of the query that needs the data the system is holding locally.

###Map Reduce
Map reduce is the pattern used to express these queries.  Map and reduce features are commonly available in functional programming languages.  Map applys a function to every data point in a set.  Reduce takes a set and reduces it a single value.

Go through notebook here.

In addition to mapping and reducing, there's also a shuffle step.  Basically, map returns the transformed data plus a bucket.  An internal function routes all of the data in the same bucket to the same reducer.  This would be helpful if you were doing something like a hash join.

Bite on Sunday after last class.
My email address.
Bring ERDs next time.  It might be worth having paper copies.