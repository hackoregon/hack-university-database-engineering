#!/bin/bash

apt-get update -y

# install firefox
apt-get install -y firefox

# install postgres
apt-get install -y postgresql
apt-get install -y pgadmin3

# cleanup
apt-get autoremove -y

# add vagrant user to postgres
su postgres -c 'psql -c "CREATE USER vagrant with CREATEUSER;"'

# add vagrant database to postgres
su postgres -c 'psql -c "CREATE database vagrant;"'

# import data into postgres
su vagrant -c 'psql < proj/buildCrimeDataRaw.sql'

echo 'run this on host machine: '
echo 'vagrant plugin install vagrant-vbguest'
