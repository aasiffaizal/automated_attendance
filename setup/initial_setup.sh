#!/bin/bash

sudo apt-get update

#configure dpkg
sudo dpkg --configure -a

#python dependencies
sudo apt install python-setuptools python-wheel

#install pip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

#install dlib dependencies
sudo apt-get install libboost-all-dev

#install django
sudo pip install django

#install matplotlib
python -mpip install matplotlib






