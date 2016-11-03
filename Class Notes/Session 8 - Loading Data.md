# Importing data

## Postgres Dump Files

BuildCrimeDataRaw.sql is a postgres dump file.  It's the format that would typically be used in a postgres database backup.

### Command Line Syntax

pg_dump -f <filename> -t <tablename>

### GUI Instructions

Right-click on DB, schema, or table and then choose Backup.  Choose plain format to create a file like BuildCrimeDataRaw.sql.

## Other File Formats

The filename does not tell you what the file format is; you need to look at the contents of the file to know.

- Delimited (csv)
- Fixed width
- XML
- JSON
- Excel
- HTML/Other

## Working With Delimited Files

### More Details

CSV files have two delimiters, quoting rules, and escaping rules.  The two delimiters are comma and the line termination character.  Line termination characters vary between the major operating systems.  ```unix2dos```, which isn't installed by default, is a good way to convert between windows and unix line termination characters.

Quoting rules and escaping rules are fairly standard and most tools you would use will understand them.  If you roll your own tool, you'll need to learn the quoting and escaping rules.

### How to decide which columns to create

Several tools can be helpful:

- the data dictionary
- head
- Your favorite text editor
- csvstat (sudo pip install csvkit)
- csvsql (included in csvkit)

### Copy Command

When you use copy from, the file needs to be on the database server.  This command can be executed from any connection to the database.  Also, the table needs to exist before calling copy.

```sql

COPY best_at FROM '/vagrant/data/best_at.csv' WITH(FORMAT CSV, HEADER);
```

### \\Copy Command

This command is only available through psql and equivalent tools.  The file needs to be on the system where psql is executed, which may or may not be the database server.

```sql

\COPY best_at FROM '/vagrant/data/best_at.csv' WITH(FORMAT CSV, HEADER);
```

### Do it in the GUI

In pgadmin3, right-click on table and choose import.  This option can't be automated easily, but it can create the table for you.

### Get Creative

There are many other ways to import data:

- Generate the insert commands yourself
- Connect through a program (e.g., a python script)
- Use standalone ETL tools
- Restore a database

### Copy To

In addition to copy from, there's also copy to that can be used to export data.  Permissions are the those of the postgres account.

```sql

COPY crimedata.crimedataraw TO '/home/vagrant/proj/crimedata.csv' WITH(FORMAT CSV, HEADER);
```

## Encoding

The encoding is what determines what a binary string means.  Postgres defaults to UTF-8, which is a good choice in the US.  Data files have all been encoded to some specification.  If it's not UTF-8 or a subset of UTF-8, you won't be able to import the file without changing the encoding.  The ```file``` command can often identify what type of coding a file used and the ```iconv``` command can let you change it.  If everything else fails, you can always use a text editor to adjust the characters that are causing you problems.

## Assignment

1. Import crime data from the text file (not the dump file like we did before).
2. Import Schools.csv into education.schools.
3. Import Performance.csv into education.performance.

### Advanced Questions

1. Create a bash script that uses wget to download schools.csv from the github site, does all necessary transformations, and then imports it into the database.
