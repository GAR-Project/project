#!/bin/bash

###################
# Install MiniNet #
###################

# Install needed dependencies.
sudo apt-get update && apt-get install -y git hping3

# Clone Mininet repo. We'll just pull the latest commit to speed things up
git clone --depth 1 https://github.com/mininet/mininet

# Install MiniNet Core, OF dependencies, OFv3 and the Ryu controller.
sudo ./mininet/util/install.sh -fnv3

# Test installation
sudo mn --test ping
