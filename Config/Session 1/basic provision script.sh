#!/bin/bash

apt-get update -y

#install firefox
apt-get install -y firefox

#cleanup
apt-get autoremove -y

echo 'run this on host machine: '
echo 'vagrant plugin install vagrant-vbguest'
