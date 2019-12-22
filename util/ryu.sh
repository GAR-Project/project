#!/usr/bin/env bash

# Update VM and get git tool
sudo apt-get update && apt-get install -y git 

# Install RYU
echo "Installing RYU..."

# install Ryu dependencies
sudo apt-get install -yq python python3 python-pip
sudo apt-get install -yq python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev
  
# fetch RYU
git clone git://github.com/osrg/ryu.git ryu
cd ryu

# install ryu
sudo pip install -r tools/pip-requires -r tools/optional-requires
sudo pip install .

