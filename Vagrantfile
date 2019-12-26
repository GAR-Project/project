# -*- mode: ruby -*-
# vi: set ft=ruby :
# encoding: UTF-8

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provider "virtualbox" do |v|
  v.customize ["modifyvm", :id, "--memory", 1024]
  end

  config.vm.define "test" do |test|
    test.vm.hostname = 'test'  
    test.vm.network :private_network,ip:"10.0.123.2"
    test.vm.provision "shell", :path => "./util/provisioning.sh"
    test.vm.provision "file", source: "./src/scenario_basic.py", destination: "/home/vagrant/scenario_basic.py"
    test.vm.provision "file", source: "./src/ddos.py", destination: "/home/vagrant/ddos.py"
  end
  
  config.vm.define "controller" do |controller|
    controller.vm.hostname = 'controller'  
    controller.vm.network :private_network,ip:"10.0.123.3"
    controller.vm.provision "shell", :path => "./util/ryu.sh"
  end
	
end
