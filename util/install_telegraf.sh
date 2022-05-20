#!/bin/bash

###########################
# Install Telegraf 1.13.0 #
###########################

# Get the appropriate package.
wget https://dl.influxdata.com/telegraf/releases/telegraf_1.13.0-1_amd64.deb

# Install it.
sudo dpkg -i telegraf_1.13.0-1_amd64.deb

# Remove it, we don't need it anymore.
rm telegraf_1.13.0-1_amd64.deb

# Backup the stock configuration
mv /etc/telegraf/telegraf.conf /etc/telegraf/telegraf.conf.bak

# And copy ours
cp conf/telegraf.conf /etc/telegraf/

# Restart Telegraf and we're good to go.
sudo systemctl restart telegraf
