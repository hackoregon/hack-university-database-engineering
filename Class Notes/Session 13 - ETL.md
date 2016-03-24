# ETL


## Overview

- What is it?
- Types of ETL
  -  Batch
  -  Realtime


## What is it?

The bright future of decision making has been, and still is making decisions using data; not solely trusting human intuition.
Analysts, scientists and statisticians have a problem, though. They want to understand data: but data is almost always inconsistent,
corrupted, missing, or just plain invalid.

That's because people are involved in data collection most of the time.

The job of an Extraction Transformation and Loading (ETL) system is to try and homogenize those data into a consistent
format so the data can be compared.

It's much like a body's digestive system. It digests information into its constituent parts, orders what it can for use and 
discards the rest. As data engineers, you're the plumbers for your organization's GI tracts.

### You're already practiced

Already you know something about ETL. Even in your first classes you were loading data into the database using the `WITH CSV` command.

You were doing ETL there! Admittedly it was a very simple workflow -- most of the work was being doing in the database, but ETL is a continuum.


### Extraction

This is where we take information in one format and pull out the bits that are useful to our purpose.

e.g. Pulling certain attributes out of a JSON object result from an API call.

### Transformation

Taking those extracted data, and putting them into whatever format we desire, correcting incorrect values where possible, possibly annotating related
information into the same destination format.

e.g. Putting the selected JSON attributes into a Protobuffer, adding identifier annotations to data in other systems.


#### Loading

Putting your data into a database for later analysis.

e.g. psql -c \COPY your_table FROM 'your_file.csv' CSV


## Types of ETL

### Batch

This is in many ways the simplest way to construct a system, and how many of the highest performance ETL systems organize their work.

One downside is that up-to-date information is only available after each batch is run.

### Realtime

This system means that you continuously update your database(s) as new information comes into your system. It's a good choice
when the requirement is that your system's information must be close to real-time.

One downside is that this is a more difficult system to scale as your data size and frequency increase.
