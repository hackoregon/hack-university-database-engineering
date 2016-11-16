# GIS and Redundancy

## Redundancy

Normalization removes redundancy from systems.  This is good.  But, sometimes, we want to have backup copies of our data.  There are several spiffy techniques regularly employed in databases (and elsewhere) to ensure that no data is lost.

### RAID-Redundant Array of Inexpensive Devices

Imagine 3 identical disks.  Disks 1 and 2 hold data.  Disk 3 hold redundancy information.  For each bit on disk 1, do an exclusive or (1 xor 1 = 0, 1 xor 0 = 1, 0 xor 0 = 0) with disk 2 and store that value on disk 3.  If any disk fails, you could reconstruct all the data.  This is almost RAID 3.  There are about a half dozen different models with different characteristics.

### Transaction Log

The database can fail at any point.  If it's updating data while it fails, there's no dependable way to know how far it had gotten in the write.  To deal with this, the DB writes everything twice.  First, it write into a sequential file called the transaction log that it's about to change some data and exactly what the change will be.  After that, it changes the data.  Last, it goes back to the transaction log and writes that it finished changing the data.  If the system doesn't fail, nothing reads from the transaction log (in regular processing).  If the system fails, you either know that it hasn't started writing yet or exactly what it was writing; both would be enough to reconstruct a stable state of the DB.  All told, this roughly doubles the amount of data written, but you can put the transaction log on separate spindles, which means there's no visible cost.

### DB Backups

If you don't want to reconstruct your data from scratch, you should back up you data now and then.  On postgres, use DB dumps for backups.  You can also store a baseline backup and all the transaction logs that have been generated since you took that backup because the transaction logs list all of the changes that were made.  On Postgres, transaction logs are recycled automatically, so you have to jump through some hoops to automatically store them.  This isn't the case on systems that expect professional DBAs to be involved.

All database systems come preinstalled with data corruption fairies.  When the fairies decide to corrupt some data, they always start with the data that you haven't backed up.  Use this fact when you decide what to backup and how often to back it up.


## Geographic Information Systems (GIS)

GIS systems track geographic data.  PostGIS is the dominant Postgres GIS package and allows us to store, query, and transform GIS info.

### Shapes

Most GIS system have a few common shapes: point, linestring (a series of connected points), polygon (a closed linestring), multipoint (basically a linestring, though a case could be made that that it should be unordered), multilinestring (a set of linestrings), multipolygon (a set of polygons), geometrycollection (a set of shapes).

```sql

CREATE TEMP TABLE geometries (name varchar, geom geometry);

INSERT INTO geometries VALUES
  ('Point', 'POINT(0 0)'),
  ('Linestring', 'LINESTRING(0 0, 1 1, 2 1, 2 2)'),
  ('Polygon', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
  ('PolygonWithHole', 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0),(1 1, 1 2, 2 2, 2 1, 1 1))'),
  ('Collection', 'GEOMETRYCOLLECTION(POINT(2 0),POLYGON((0 0, 1 0, 1 1, 0 1, 0 0)))');

SELECT name, ST_ASTEXT(geom)
FROM geometries;

SELECT name, ST_AREA(geom)
FROM geometries
```

### Geometry v Geography

Geometry is spatial data in a linear universe (pre-gallilean geography).  Geography is spatial data in a spherical universe (post-gallilean geography).

Distance calculation using GEOGRAPHY (122.2km)
```sql

SELECT ST_DISTANCE('LINESTRING(-122.33 47.606, 0.0 51.5)'::GEOGRAPHY, 'POINT(-21.96 64.15)':: GEOGRAPHY);
```

Distance calculation using GEOMETRY (13.3 "degrees")
```sql

SELECT ST_DISTANCE('LINESTRING(-122.33 47.606, 0.0 51.5)'::GEOMETRY, 'POINT(-21.96 64.15)':: GEOMETRY);
```

You can see that calculation on a map at http://gc.kls2.com/cgi-bin/gc?PATH=SEA-LHR

Shapes exist as both geometries and geographies.  Math on geometry is easier, so there are more functions there.  There are GIS applications for both geographies (e.g., maps) and geometries (e.g., 3d models).

### Coordinate Systems

Coordinate systems are how we represent a 3 dimensional round surface on 2 dimensions.  Two examples are Latitude/Longitude and the Oregon Coordinate Reference System.  Our crimedata used the Oregon Coordinate Reference System.

All commonly used coordinate systems have a Spatial Reference System Identifier SRID, which is a number that uniquely identifies how to translate between this system and 3 dimensions.

PostGIS only supports SRID 4326 (lat/long) as of v 2.1

If the SRIDs of two sets of data aren't the same, the data isn't compatible and you can't combine the two sets until you've resolved the difference.

### Shape Files

.shp (pronounced like shape) files were an early technology used for GIS storage.  They are commonly used in proprietary systems and for information exchange.  Shape files come with a entourage including .shp and .prj files. Prj files store the details about the coordinate system and can be sent to http://prj2epsg.org/search to determine SRID.  Other files typically loaded automatically with the shp file.

### PostGIS

PostGIS is extension an extension to Postgres similar to how plpython3u is an extension, so you'll need to activate it in each database that will use it.  This command will do that for you.

```sql

CREATE EXTENSION postgis;
```

PostGIS includes the ability to store GIS data, a set of functions that work on that data, the ability to index that data, and tools for importing/exporting the data.

Our install didn't include all of the binaries needed, so please add this to your config file.  While we're add it, we should also add unzip.

```bash

apt-get install postgis
apt-get install unzip
```

#### Functions

##### Querying Functions

- ST_GeometryType - returns the type of a shape.
- ST_NDims - returns the dimensionality of a shape.
- ST_SRID - returns the SRID of a shape.

##### Input/Output Functions

- ST_AsText - returns a shape as a human readable text string.
- ST_GeomFromText - creates a shape from text.
- ST_AsSVG - returns a shape as a Support Vector Graphic (can be used on webpages).

```
'POINT(0 0)'::geometry
```
is a shorthand for
```
ST_GeomFromText('POINT(0 0)')
```

##### Shape Specific Functions

- ST_X - returns the x coordinate of a point.
- ST_Y - returns the y coordinate of a point.
- ST_NPoints - returns the number of points in a shape.
- ST_Length - returns the length of a linestring.
- ST_PointN - returns the nth point of a linestring.
- ST_Area - returns the area of a polygon.
- ST_NRings - returns the number of rings in a polygon (1 for simple polygons).
- ST_InteriorRingN - returns the nth ring as a linestring.
- ST_NumGeometries - returns the number of geometries of a geometry set.
- ST_GeometryN - returns the nth geometry in a set.

##### Functions on Multiple Shapes

- ST_Equals - returns TRUE iff the types and their dimensions are identical.
- ST_Intersects - returns TRUE iff the two shapes share some space.
- ST_Crosses - returns TRUE iff the two shapes cross.
- ST_Overlaps - returns TRUE iff the two shapes overlap.
- ST_Within - returns TRUE iff the first shape is completely contained within the second shape.
- ST_Contains - returns TRUE iff the second shape is completely contained within the first shape.
- ST_Distance - returns the shortest distance between the two shapes.

#### Spatial Joins

Remember that joins can use any test that feels appropriate, not just testing if two IDs are equal.  So this is a completely valid join:

```sql

SELECT *
FROM osm.streets s1 inner join osm.streets s2
  ON ST_Crosses(s1.geom, s2.geom);
```

#### Import/Export

Most of the import/export tools for standard Postgres will work with a database that has PostGIS activated.  We will use shp2pgsql for our imports, because it can convert from shapefiles.  There's a plugin for this tool that makes it worth with pgadmin3, but we won't be spending enough time with it to make it worth the time to set it up.

#### Documentation

There are some good tutorials (e.g., http://workshops.boundlessgeo.com/postgis-intro/index.html) and other documentation (http://postgis.net/documentation/) available if you get called on to do more in PostGIS.  This lecture was inspired by the boundlessgeo tutorial.


### Open Street Map

We need some data to work with.  One useful source is the Open Street Map project (https://www.openstreetmap.org/).  There are some limits to the extract rules from that site, however, so it might be easier to go to a site that already has Portland extracted for us (https://mapzen.com/data/metro-extracts/metro/portland_oregon/).  For this exercise, choose the IMPOSM SHAPEFILE.

#### Import osm

Save the zip file to ~/proj/data and then run ```unzip portland_oregon.imposm-shapefiles.zip``` to extract the files.

In pgadmin3, create a schema for the osm by running ```CREATE SCHEMA osm;``` and, if the postgis extension has been activated for your database yet, run ```CREATE EXTENSION postgis;```.

Convert the shape file to sql by running ```shp2pgsql portland_oregon_osm_roads osm.roads > loadRoads.sql```.  Last, execute ```psql < loadRoads.sql``` to import this data into the database.  Both of these commands will take most of a minute to run and will look like they've hung.

--Find Glisan
SELECT DISTINCT name
FROM osm.roads
WHERE UPPER(name) like UPPER('%Glisan%')

SELECT *
FROM osm.roads
WHERE name = 'Northwest Glisan Street'

### General Transit Feed Specification

Download gtfs.zip from https://developer.trimet.org/GTFS.shtml and store it in ~/proj/data/gtfs.  Run ```unzip gtfs.zip``` there to extract the files.

Import shapes.txt (it's a csv) into gtfs.shapes_raw.

```sql

CREATE SCHEMA gtfs;
CREATE TABLE gtfs.shapes_raw (
	shape_id INTEGER NOT NULL,
	shape_pt_lat FLOAT NOT NULL,
	shape_pt_lon FLOAT NOT NULL,
	shape_pt_sequence INTEGER NOT NULL,
	shape_dist_traveled FLOAT NOT NULL
);

COPY gtfs.shapes_raw FROM '/home/vagrant/proj/data/gtfs/shapes.txt' WITH (FORMAT CSV, HEADER);
```

Each point of a line shows up as its own record, we'd rather see the data combined.
```sql

SELECT shape_id, ST_MakeLine(ST_SetSRID(ST_MakePoint(shape_pt_lon, shape_pt_lat), 4326) ORDER BY shape_pt_sequence) as shape
INTO gtfs.shapes
FROM gtfs.shapes_raw
GROUP BY shape_id
```

It's good to understand what this query is doing.  ST_MakeLine is an aggregation function and is combining multiple records of data into one.  The order by is important because we want to ensure that the linestring connects consecutive points and not random points.

GTFS is a standard and there are a fair number of tools to work with them, if you end up needing to.

You'll also need to import trips.txt for the harder question.

```sql

CREATE TABLE gtfs.trips (
	route_id INTEGER NOT NULL,
	service_id VARCHAR(5) NOT NULL,
	trip_id INTEGER NOT NULL,
	direction_id INTEGER NOT NULL,
	block_id INTEGER NOT NULL,
	shape_id INTEGER NOT NULL,
	trip_type VARCHAR(7)
);

COPY gtfs.trips FROM '/home/vagrant/proj/data/gtfs/trips.txt' WITH (FORMAT CSV, HEADER);
```

### Geocoders

Geocoders are software that take addresses and convert them to coordinates.  Addresses should be standardized before using a geocoder.

Geocoders are much easier to use than to setup.

## Harder Assignment

1. Find all streets that intersect NW Glisan.
2. What bus routes pass 321 NW Glisan St?  You'll need data from trips.txt for this question.
