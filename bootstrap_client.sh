#!/usr/bin/env bash

apt-get update
apt-get install -y build-essential
apt-get install -y git
apt-get install -y vim
apt-get install -y python-pip
apt-get install -y fabric
apt-get install -y python-nose
apt-get install -y python-yaml

cp /vagrant/insecure_vagrant_private_key.txt /home/vagrant/.ssh/id_rsa
chown vagrant /home/vagrant/.ssh/id_rsa
chmod 600 /home/vagrant/.ssh/id_rsa

touch /home/vagrant/.ssh/known_hosts
ssh-keyscan -t rsa,dsa 10.10.10.11 2>&1 | sort -u - /home/vagrant/.ssh/known_hosts > /home/vagrant/.ssh/tmp_hosts
cat /home/vagrant/.ssh/tmp_hosts >> /home/vagrant/.ssh/known_hosts

# Ensure the .bash_profile file exists.

touch ~/.bash_profile

# Setup the python path.

if ! grep -Fxq "export PYTHONPATH=/vagrant" ~/.bash_profile
then
    echo "export PYTHONPATH=/vagrant" >> ~/.bash_profile
    export export PYTHONPATH=/vagrant
fi
