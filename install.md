# Setup your system

We will use Vagrant and Virtual Box so all of our systems will behave identically.

#### Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

Virtual Box allows you to run a small linux computer within your laptop!  Find the right package for your OS and install it:

- [Ubuntu 15.03](http://download.virtualbox.org/virtualbox/5.0.14/virtualbox-5.0_5.0.14-105127~Ubuntu~wily_amd64.deb)
- [any Linux](https://www.virtualbox.org/wiki/Linux_Downloads)
- [OSX](http://download.virtualbox.org/virtualbox/5.0.14/VirtualBox-5.0.14-105127-OSX.dmg)
- [Win64](http://download.virtualbox.org/virtualbox/5.0.14/VirtualBox-5.0.14-105127-Win.exe)

#### Download [Vagrant](https://www.vagrantup.com/downloads.html)

Vagrant is a system that allows you to automate a lot of the process involved in configuring and controlling virtual machines on your laptop.

Go to the Vagrant [download page](https://www.vagrantup.com/downloads.html) to find the installation package for your OS. Download the package and double click it to open it with your package manager (software installer). On Ubuntu, the "Software Center" will launch and you click either the orange "Install" or "Upgrade" button.

#### Mac Only

Download and install [XQuartz](https://www.xquartz.org/).

#### Windows Only

[This site](https://wiki.utdallas.edu/wiki/display/FAQ/X11+Forwarding+using+Xming+and+PuTTY) has fairly accurate documentation of what we'll be doing.  You won't be able to make the connection until your vagrant box is setup

Download [PuTTy](http://www.putty.org/)

This is tool allows you to open a shell session to your virtual box.  

Download [Xming](https://sourceforge.net/projects/xming/)

This allows you to open a GUI session from your virtual box.  Before running PuTTy, always launch Xming.


#### Setup first Vagrant Box
If you want to start your vagrant box from scratch, create a directory and execute the following commands from within that directory
```
vagrant init ubuntu/trusty64
vagrant up
```

For this class, you won't be creating a new vagrant box and should download the two files [here](Config/Session 1) into a new folder and then execute these commands in that folder.

```
vagrant up
vagrant ssh
firefox
```

If everything worked correctly, you should now see a new firefox window with a title "Firefox on vagrant".

These instructions were adapted from the instructions put together for a [previous version of Machine Learning](https://github.com/hackoregon/hack-university-machine-learning/blob/master/docs/install.md)
