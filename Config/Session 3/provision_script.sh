#!/bin/bash

apt-get update -y

#install firefox
apt-get install -y firefox

#install postgres
apt-get install -y postgresql

#install pgadmin
apt-get install -y pgadmin3

#cleanup
apt-get autoremove -y

echo 'run this on host machine: '
echo 'vagrant plugin install vagrant-vbguest'
