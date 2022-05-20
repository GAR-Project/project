#!/bin/bash

#####################################
# Bootstrap Grafana's configuration #
#####################################

# Move the existing data source's (i.e. InfluxDB) configuration so that Grafana picks it up 'automagically'
sudo mv datasources.yaml /etc/grafana/provisioning/datasources/datasources.yaml

# Crate the bootstrapping directory for dashboards
sudo mkdir /var/lib/grafana/dashboards

# And copy the preexisting dashoboards over for Grafana to pick up
sudo cp project.json /var/lib/grafana/dashboards/
sudo cp main.yaml /etc/grafana/provisioning/dashboards/main.yaml

# Restart Grafana so that it picks up the above
sudo systemctl restart grafana-server
