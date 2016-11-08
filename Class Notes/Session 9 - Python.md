# Python in Postgresql

## Apt-get Repositories

Your system has a list of repositories that it trusts.  The following command lists all of the repositories that your system currently trusts.

```bash

apt-cache policy
```

By default, your system mostly trusts repositories that have software that has been vetted by Canonical.  It takes a while to do that validation, so you sometimes need to look elsewhere to find more recent software.  One option is to download the source files and build the software (this is really a thing on \*nix).  Another option is to manually download install files.  A third option is to trust more repositories.  We'll use the third option in this class.

## Postgres 9.5

During the GIS class, we'll need a product called postgis.  There's a repository that includes recent builds of postgres and postgis.  We'll manually add that repository and use it to install Postgres 9.5.  The following code adds that new repository and updates our cache of apps.

```bash

#add postgis to list of trusted repositories
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt trusty-pgdg main" >> /etc/apt/sources.list'
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
apt-get update -y
apt-get upgrade -y
```

This code takes gets the right version of postgres and the libraries that we'll want today and Wednesday.

```bash

#install postgrest, postgis, and pgadmin3
apt-get install -y postgresql-9.5-postgis-2.2 pgadmin3

# Install pgRouting 2.1 package
apt-get install -y postgresql-9.5-pgrouting

#install python for postgres
apt-get install -y postgresql-plpython3-9.5
```

## Telling Postgres to Use Python

Postgres knows about PLPGSQL by default, but no other languages.  We just installed an extension in the operating system that allows us to use python in postgres, but we need to activate it in each database that will use it.  This command enables the python extension.  We're using Python 3 here.  There's a version for python 2, but it's better to stick to python 3 unless you have a compelling reason to use python 2.

```sql

CREATE EXTENSION plpython3u;
```

## Python Super Fast Intro

- There are no curly brackets, the indent defines the block of code.
- To create and/or assign to a variable say ```var=val```
- Outside of complex data types, data types are automatically determined in python (int v string)
- Python supports tuples: (1, 2), lists [1, 2, 3], and dictionaries {"name": "value"}.  Tuples are static, the other two are dynamic.
- Indexing in python is flexible and powerful "123456"[2:-1] pulls out the 3rd character through the second to the last character.
- Python has standard flow control functions and the : character is the flag that the indent level will increase (a new block of code is required).
- There are common functional idioms in python, like list comprehension: [x*100 for x in range(10)] is the same as [0, 100, 200, 300, 400, 500, 600, 700, 800, 900].

## Compile/Execution Time Validation

Though the languages we're using don't have a compile phase, the database performs similar steps when you create a function.

When you declare a function, you need to specify input types and return types.  There are several ways to declare the return types.  You can use standard types, which we're familiar with (e.g., varchar), you can use custom types, you can use dynamic types, and you can punt.  In addition, you need to specify if the function will return exactly 1 result (the default), or if it can return any number of results.

### Standard Types

Function declarations that return standard types are the easiest to read.

```sql

CREATE OR REPLACE FUNCTION reverse_string(inval VARCHAR)
  RETURNS varchar
AS $$
return inval[::-1]
$$ LANGUAGE plpython3u;

SELECT reverse_string('read me backwards');
```

### Custom Types

You can return existing types/table rows.

```sql

SELECT major_offense_type, address, neighborhood
INTO crimedata.small_table
FROM crimedata.crimedataraw
LIMIT 1;

CREATE OR REPLACE FUNCTION get_small_table_data()
  RETURNS SETOF crimedata.small_table
AS $$
return [["saying mean things", "here", "pearl"]]
$$ LANGUAGE plpython3u;

SELECT * FROM get_small_table_data();
```

### Dynamic Types

```sql

CREATE OR REPLACE FUNCTION two_columns()
  RETURNS TABLE (col1 varchar, col2 varchar)
AS $$
return [["I'm in column 1", "I'm in column 2"],
	["second row", "second row"]]
$$ LANGUAGE plpython3u;

SELECT * FROM two_columns();
```

### Punting

```sql

CREATE OR REPLACE FUNCTION n_cols(n int)
  RETURNS SETOF RECORD
AS $$
return [[x for x in range(n)]]
$$ LANGUAGE plpython3u;

SELECT * FROM n_cols(2) AS (c1 text, c2 int);
```


## Other Details

plpy is defined in your python function and can be used to access the database.  It's also possible to statically share data between instances of your function and also between all python functions on the system.

Also, postgres and python make reasonable assumptions about how to convert data.  There are multiple ways to pass data back and in most cases the system will do what you expect.

## Loading Census Data

The census bureau publishes lots of data.  To use it, you'll need to invest a non-trivial amount of time in reading the documentation.  I've included the key documentation in the data section; not so you can read it, but so you can understand what these challenges take when you encounter them on your own.  This particular dataset includes both a csv file and a fixed width text file.  Both files need to be parsed and then combined before you can fully query the data.

I created the ods file by using copy and paste from one of the pdfs, correcting any errors, and then applying formulas.

The ods file was used to generate both the table definitions and the list used in the parsing formula.  I find this model of importing as raw text easier than trying to parse during the import process.

This command installs unzip, which can be used to decompress the datafile.

```bash

sudo apt-get install unzip
```

```sql

create schema census;

create table census.orgeo2010p1raw
(
	raw varchar
);

copy census.orgeo2010p1raw FROM '/home/vagrant/proj/data/censusdata/or/orgeo2010.dp' WITH(FORMAT TEXT);
```
This creates the parsed table.

```sql

create table census.orgeo2010p1
(
FILEID varchar,
STUSAB varchar,
SUMLEV varchar,
GEOCOMP varchar,
CHARITER varchar,
CIFSN varchar,
LOGRECNO int,
REGION varchar,
DIVISION varchar,
STATE varchar,
COUNTY varchar,
COUNTYCC varchar,
COUNTYSC varchar,
COUSUB varchar,
COUSUBCC varchar,
COUSUBSC varchar,
PLACE varchar,
PLACECC varchar,
PLACESC varchar,
TRACT varchar,
BLKGRP varchar,
BLOCK varchar,
IUC varchar,
CONCIT varchar,
CONCITCC varchar,
CONCITSC varchar,
AIANHH varchar,
AIANHHFP varchar,
AIANHHCC varchar,
AIHHTLI varchar,
AITSCE varchar,
AITS varchar,
AITSCC varchar,
TTRACT varchar,
TBLKGRP varchar,
ANRC varchar,
ANRCCC varchar,
CBSA varchar,
CBSASC varchar,
METDIV varchar,
CSA varchar,
NECTA varchar,
NECTASC varchar,
NECTADIV varchar,
CNECTA varchar,
CBSAPCI varchar,
NECTAPCI varchar,
UA varchar,
UASC varchar,
UATYPE varchar,
UR varchar,
CD varchar,
SLDU varchar,
SLDL varchar,
VTD varchar,
VTDI varchar,
RESERVE2 varchar,
ZCTA5 varchar,
SUBMCD varchar,
SUBMCDCC varchar,
SDELM varchar,
SDSEC varchar,
SDUNI varchar,
AREALAND varchar,
AREAWATR varchar,
NAME varchar,
FUNCSTAT varchar,
GCUNI varchar,
POP100 varchar,
HU100 varchar,
INTPTLAT varchar,
INTPTLON varchar,
LSADC varchar,
PARTFLAG varchar,
RESERVE3 varchar,
UGA varchar,
STATENS varchar,
COUNTYNS varchar,
COUSUBNS varchar,
PLACENS varchar,
CONCITNS varchar,
AIANHHNS varchar,
AITSNS varchar,
ANRCNS varchar,
SUBMCDNS varchar,
CD113 varchar,
CD114 varchar,
CD115 varchar,
SLDU2 varchar,
SLDU3 varchar,
SLDU4 varchar,
SLDL2 varchar,
SLDL3 varchar,
SLDL4 varchar,
AIANHHSC varchar,
CSASC varchar,
CNECTASC varchar,
MEMI varchar,
NMEMI varchar,
PUMA varchar,
RESERVED varchar,
constraint census_orgeo2010p1_pk primary key (logrecno)
)
```

This populates the parsed table with data.  This version is longer, but much easier to understand than my version from class.  The class version is also included below.

```sql

CREATE OR REPLACE FUNCTION census.parse_geo_info (r varchar)
	RETURNS census.orgeo2010p1
AS $$
lengths = [['FILEID', 0, 6],
	['STUSAB', 6, 8],
	['SUMLEV', 8, 11],
	['GEOCOMP', 11, 13],
	['CHARITER', 13, 16],
	['CIFSN', 16, 18],
	['LOGRECNO', 18, 25],
	['REGION', 25, 26],
	['DIVISION', 26, 27],
	['STATE', 27, 29],
	['COUNTY', 29, 32],
	['COUNTYCC', 32, 34],
	['COUNTYSC', 34, 36],
	['COUSUB', 36, 41],
	['COUSUBCC', 41, 43],
	['COUSUBSC', 43, 45],
	['PLACE', 45, 50],
	['PLACECC', 50, 52],
	['PLACESC', 52, 54],
	['TRACT', 54, 60],
	['BLKGRP', 60, 61],
	['BLOCK', 61, 65],
	['IUC', 65, 67],
	['CONCIT', 67, 72],
	['CONCITCC', 72, 74],
	['CONCITSC', 74, 76],
	['AIANHH', 76, 80],
	['AIANHHFP', 80, 85],
	['AIANHHCC', 85, 87],
	['AIHHTLI', 87, 88],
	['AITSCE', 88, 91],
	['AITS', 91, 96],
	['AITSCC', 96, 98],
	['TTRACT', 98, 104],
	['TBLKGRP', 104, 105],
	['ANRC', 105, 110],
	['ANRCCC', 110, 112],
	['CBSA', 112, 117],
	['CBSASC', 117, 119],
	['METDIV', 119, 124],
	['CSA', 124, 127],
	['NECTA', 127, 132],
	['NECTASC', 132, 134],
	['NECTADIV', 134, 139],
	['CNECTA', 139, 142],
	['CBSAPCI', 142, 143],
	['NECTAPCI', 143, 144],
	['UA', 144, 149],
	['UASC', 149, 151],
	['UATYPE', 151, 152],
	['UR', 152, 153],
	['CD', 153, 155],
	['SLDU', 155, 158],
	['SLDL', 158, 161],
	['VTD', 161, 167],
	['VTDI', 167, 168],
	['RESERVE2', 168, 171],
	['ZCTA5', 171, 176],
	['SUBMCD', 176, 181],
	['SUBMCDCC', 181, 183],
	['SDELM', 183, 188],
	['SDSEC', 188, 193],
	['SDUNI', 193, 198],
	['AREALAND', 198, 212],
	['AREAWATR', 212, 226],
	['NAME', 226, 316],
	['FUNCSTAT', 316, 317],
	['GCUNI', 317, 318],
	['POP100', 318, 327],
	['HU100', 327, 336],
	['INTPTLAT', 336, 347],
	['INTPTLON', 347, 359],
	['LSADC', 359, 361],
	['PARTFLAG', 361, 362],
	['RESERVE3', 362, 368],
	['UGA', 368, 373],
	['STATENS', 373, 381],
	['COUNTYNS', 381, 389],
	['COUSUBNS', 389, 397],
	['PLACENS', 397, 405],
	['CONCITNS', 405, 413],
	['AIANHHNS', 413, 421],
	['AITSNS', 421, 429],
	['ANRCNS', 429, 437],
	['SUBMCDNS', 437, 445],
	['CD113', 445, 447],
	['CD114', 447, 449],
	['CD115', 449, 451],
	['SLDU2', 451, 454],
	['SLDU3', 454, 457],
	['SLDU4', 457, 460],
	['SLDL2', 460, 463],
	['SLDL3', 463, 466],
	['SLDL4', 466, 469],
	['AIANHHSC', 469, 471],
	['CSASC', 471, 473],
	['CNECTASC', 473, 475],
	['MEMI', 475, 476],
	['NMEMI', 476, 477],
	['PUMA', 477, 482],
	['RESERVED', 482, 500]
	]
returnval = []
for (name, start, end) in lengths:
	returnval.append(r[start:end])
return returnval
$$ LANGUAGE plpython3u;

insert into census.orgeo2010p1
select p.*
from census.orgeo2010p1raw r, census.parse_geo_info(raw) p
```

Don't run this code, but it's the version that I used in class.

```sql

CREATE OR REPLACE FUNCTION census.parse_geo_info (r varchar)
	RETURNS census.orgeo2010p1
AS $$
	lengths = [0,6,8,11,13,16,18,25,26,27,29,32,34,36,41,43,45,50,52,54,60,61,65,67,72,74,76,80,85,87,88,91,96,98,104,105,110,112,117,119,124,127,132,134,139,142,143,144,149,151,152,153,155,158,161,167,168,171,176,181,183,188,193,198,212,226,316,317,318,327,336,347,359,361,362,368,373,381,389,397,405,413,421,429,437,445,447,449,451,454,457,460,463,466,469,471,473,475,476,477,482,500]
	return [r[lengths[i-1]:lengths[i]] for i in range(1, len(lengths))]
$$ LANGUAGE plpython3u;

```

This code creates the second raw table.

```sql

CREATE TABLE census.orgeo2010p2raw
(
FILEID varchar(6),
STUSAB varchar(2),
CHARITER varchar(3),
CIFSN varchar(2),
LOGRECNO int,
pop_total int,
pop_under5 int,
pop_under10 int,
pop_under15 int,
pop_under20 int,
pop_under25 int,
pop_under30 int,
pop_under35 int,
pop_under40 int,
pop_under45 int,
pop_under50 int,
pop_under55 int,
pop_under60 int,
pop_under65 int,
pop_under70 int,
pop_under75 int,
pop_under80 int,
pop_under85 int,
pop_over85 int,
male_total int,
male_under5 int,
male_under10 int,
male_under15 int,
male_under20 int,
male_under25 int,
male_under30 int,
male_under35 int,
male_under40 int,
male_under45 int,
male_under50 int,
male_under55 int,
male_under60 int,
male_under65 int,
male_under70 int,
male_under75 int,
male_under80 int,
male_under85 int,
male_over85 int,
female_total int,
female_under5 int,
female_under10 int,
female_under15 int,
female_under20 int,
female_under25 int,
female_under30 int,
female_under35 int,
female_under40 int,
female_under45 int,
female_under50 int,
female_under55 int,
female_under60 int,
female_under65 int,
female_under70 int,
female_under75 int,
female_under80 int,
female_under85 int,
female_over85 int,
median_pop_age float,
median_male_age float,
median_female_age float,
pop_over16 int,
male_over16 int,
female_over16 int,
pop_over18 int,
male_over18 int,
female_over18 int,
pop_over21 int,
male_over21 int,
female_over21 int,
pop_over62 int,
male_over62 int,
female_over62 int,
pop_over65 int,
male_over65 int,
female_over65 int,
total int,
single_race int,
single_race_white int,
single_race_black int,
single_race_native int,
single_race_asian int,
asian_indian int,
asian_chinese int,
asian_filipino int,
asian_japanese int,
asian_korean int,
asian_vietnamese int,
asian_other int,
islander int,
islander_hawaiian int,
islander_guamanian int,
islander_samoan int,
islander_other int,
other_single_race int,
mixed_race int,
mixed_race_w_native int,
mixed_race_w_asian int,
mixed_race_w_black int,
mixed_race_w_other int,
dpsf0090001  int,
dpsf0090002 int,
dpsf0090003 int,
dpsf0090004 int,
dpsf0090005 int,
dpsf0090006 int,
 dpsf0100001  int,
 dpsf0100002 int,
 dpsf0100003 int,
 dpsf0100004 int,
 dpsf0100005 int,
 dpsf0100006 int,
 dpsf0100007 int,
 dpsf0110001  int,
 dpsf0110002 int,
 dpsf0110003 int,
 dpsf0110004 int,
 dpsf0110005 int,
 dpsf0110006 int,
 dpsf0110007 int,
 dpsf0110008 int,
 dpsf0110009 int,
 dpsf0110010 int,
 dpsf0110011 int,
 dpsf0110012 int,
 dpsf0110013 int,
 dpsf0110014 int,
 dpsf0110015 int,
 dpsf0110016 int,
 dpsf0110017 int,
rel_total int,
in_households int,
householder int,
spouse int,
child int,
own_child_under18 int,
other_relatives int,
other_relatives_under18 int,
other_relatives_over65 int,
nonrelatives int,
nonrelatives_under18 int,
nonrelatives_over65 int,
unmarried_partner int,
in_group_quarters int,
institutionalized int,
institutionalized_male int,
institutionalized_female int,
noninstitutionalized int,
noninstitutionalized_male int,
noninstitutionalized_female int,
households int,
households_family int,
households_family_with_kids int,
households_family_traditional int,
households_family_traditional_with_kids int,
households_male int,
households_male_with_kids int,
households_female int,
households_female_with_kids int,
households_nonfamily int,
householder_living_alone int,
householder_living_alone_male int,
householder_living_alone_male_over65 int,
householder_living_alone_female int,
householder_living_alone_female_over65 int,
households_with_kids int,
households_with_over65 int,
household_average_size float,
household_family_average_size float,
housing_units int,
housing_units_occupied int,
housing_units_vacant int,
housing_units_vacant_for_rent int,
housing_units_rented_not_occupied int,
housing_units_for_sale int,
housing_units_sold_not_occupied int,
housing_units_seasonal int,
housing_units_other_vacancies int,
vacancy_rate_homeowner float,
vacancy_rate_rental float,
occupied_units_total int,
occupied_units_owner int,
occupied_units_renter int,
occupied_pop_owner int,
occupied_pop_renter int,
owner_occupied_household_size float,
renter_occupied_household_size float,
constraint census_orgeo2010p2raw_pk primary key (LOGRECNO)
);
```

This command loads the data into the second part.

```sql

COPY census.orgeo2010p2raw FROM '/home/vagrant/proj/data/censusdata/or/or000012010.dp' WITH(FORMAT CSV);
```

This command was used to generate the join statement with a near complete list of fields to join.  It doesn't modify any data.

```sql

select 'l' || '.' || column_name || ','
	from information_schema.columns
	where table_schema = 'census'
		and table_name = 'orgeo2010p2raw'
		and column_name not in ('fileid', 'stusab', 'sumlev', 'geocomp', 'chariter', 'cifsn', 'logrecno');
```

This last query combines the two datasets into one table.

```sql

select r.*, l.pop_total,
l.pop_under5,
l.pop_under10,
l.pop_under15,
l.pop_under20,
l.pop_under25,
l.pop_under30,
l.pop_under35,
l.pop_under40,
l.pop_under45,
l.pop_under50,
l.pop_under55,
l.pop_under60,
l.pop_under65,
l.pop_under70,
l.pop_under75,
l.pop_under80,
l.pop_under85,
l.pop_over85,
l.male_total,
l.male_under5,
l.male_under10,
l.male_under15,
l.male_under20,
l.male_under25,
l.male_under30,
l.male_under35,
l.male_under40,
l.male_under45,
l.male_under50,
l.male_under55,
l.male_under60,
l.male_under65,
l.male_under70,
l.male_under75,
l.male_under80,
l.male_under85,
l.male_over85,
l.female_total,
l.female_under5,
l.female_under10,
l.female_under15,
l.female_under20,
l.female_under25,
l.female_under30,
l.female_under35,
l.female_under40,
l.female_under45,
l.female_under50,
l.female_under55,
l.female_under60,
l.female_under65,
l.female_under70,
l.female_under75,
l.female_under80,
l.female_under85,
l.female_over85,
l.median_pop_age,
l.median_male_age,
l.median_female_age,
l.pop_over16,
l.male_over16,
l.female_over16,
l.pop_over18,
l.male_over18,
l.female_over18,
l.pop_over21,
l.male_over21,
l.female_over21,
l.pop_over62,
l.male_over62,
l.female_over62,
l.pop_over65,
l.male_over65,
l.female_over65,
l.total,
l.single_race,
l.single_race_white,
l.single_race_black,
l.single_race_native,
l.single_race_asian,
l.asian_indian,
l.asian_chinese,
l.asian_filipino,
l.asian_japanese,
l.asian_korean,
l.asian_vietnamese,
l.asian_other,
l.islander,
l.islander_hawaiian,
l.islander_guamanian,
l.islander_samoan,
l.islander_other,
l.other_single_race,
l.mixed_race,
l.mixed_race_w_native,
l.mixed_race_w_asian,
l.mixed_race_w_black,
l.mixed_race_w_other,
l.dpsf0090001,
l.dpsf0090002,
l.dpsf0090003,
l.dpsf0090004,
l.dpsf0090005,
l.dpsf0090006,
l.dpsf0100001,
l.dpsf0100002,
l.dpsf0100003,
l.dpsf0100004,
l.dpsf0100005,
l.dpsf0100006,
l.dpsf0100007,
l.dpsf0110001,
l.dpsf0110002,
l.dpsf0110003,
l.dpsf0110004,
l.dpsf0110005,
l.dpsf0110006,
l.dpsf0110007,
l.dpsf0110008,
l.dpsf0110009,
l.dpsf0110010,
l.dpsf0110011,
l.dpsf0110012,
l.dpsf0110013,
l.dpsf0110014,
l.dpsf0110015,
l.dpsf0110016,
l.dpsf0110017,
l.rel_total,
l.in_households,
l.householder,
l.spouse,
l.child,
l.own_child_under18,
l.other_relatives,
l.other_relatives_under18,
l.other_relatives_over65,
l.nonrelatives,
l.nonrelatives_under18,
l.nonrelatives_over65,
l.unmarried_partner,
l.in_group_quarters,
l.institutionalized,
l.institutionalized_male,
l.institutionalized_female,
l.noninstitutionalized,
l.noninstitutionalized_male,
l.noninstitutionalized_female,
l.households,
l.households_family,
l.households_family_with_kids,
l.households_family_traditional,
l.households_family_traditional_with_kids,
l.households_male,
l.households_male_with_kids,
l.households_female,
l.households_female_with_kids,
l.households_nonfamily,
l.householder_living_alone,
l.householder_living_alone_male,
l.householder_living_alone_male_over65,
l.householder_living_alone_female,
l.householder_living_alone_female_over65,
l.households_with_kids,
l.households_with_over65,
l.household_average_size,
l.household_family_average_size,
l.housing_units,
l.housing_units_occupied,
l.housing_units_vacant,
l.housing_units_vacant_for_rent,
l.housing_units_rented_not_occupied,
l.housing_units_for_sale,
l.housing_units_sold_not_occupied,
l.housing_units_seasonal,
l.housing_units_other_vacancies,
l.vacancy_rate_homeowner,
l.vacancy_rate_rental,
l.occupied_units_total,
l.occupied_units_owner,
l.occupied_units_renter,
l.occupied_pop_owner,
l.occupied_pop_renter,
l.owner_occupied_household_size,
l.renter_occupied_household_size
into census.orgeo2010
from census.orgeo2010p2raw l inner join census.orgeo2010p1 r
	on l.logrecno = r.logrecno;
```

## Assignment

1. Write a python function called py_max that accept two ints and returns the greater of them.
2. Write a python function that returns 10 random numbers as separate rows.  The following code snippet returns a random number.

```python

import random
random.random()
```

### Harder Assignment

1. Walk through all of the steps of the census data import on your own and confirm that you can make them work.  What population center in Oregon has the highest fraction of people over 65 years of age?

The datafile includes person once per sumlevel.  Limit your search to sumlevel 160 (the city level).
