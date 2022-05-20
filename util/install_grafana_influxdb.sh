#!/bin/bash

#########################
# Install Grafana 6.5.2 #
#########################

# Fix borken packages and install needed dependencies.
sudo apt-get -fy install && apt-get install -y libfontconfig1

# Download the `*.deb` packaging Grafana.
wget https://dl.grafana.com/oss/release/grafana_6.5.2_amd64.deb

# Install it.
sudo dpkg -i grafana_6.5.2_amd64.deb

# Start the service (it's stopped by default).
sudo systemctl start grafana-server

# And remove the downloaded package, we don't need it any more.
rm grafana_6.5.2_amd64.deb

##########################
# Install InfluxDB 1.7.9 #
##########################

# Dowanload the appropriate package.
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.9_amd64.deb

# Install it.
sudo dpkg -i influxdb_1.7.9_amd64.deb

# Install InfluxDB's Python library. The SVM classifier uses it!
sudo apt-get update && apt-get install -yq python3-influxdb

# Start InfluxDB.
sudo systemctl start influxd

# And remove the uneeded package.
rm influxdb_1.7.9_amd64.deb
