#!/bin/bash

sudo apt-get update && apt-get install -y git hping3

# Clone Mininet Repo
git clone https://github.com/mininet/mininet

# Install Mininet core, OF dep, OFv3 and Ryu controller
sudo ./mininet/util/install.sh -fnv3

# Test installation 
sudo mn --test ping

 
