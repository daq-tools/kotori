Vagrant.configure("2") do |config|

  config.vm.define "daqzilla-debian10" do |machine|

    machine.vm.box = "generic/debian10"
    machine.vm.hostname = 'daqzilla-debian10'

    machine.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "daqzilla-debian10"]
    end

  end

  config.vm.define "daqzilla-ubuntu18" do |machine|

    machine.vm.box = "ubuntu/bionic64"
    machine.vm.hostname = 'daqzilla-ubuntu18'

    machine.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 2048]
      v.customize ["modifyvm", :id, "--name", "daqzilla-ubuntu18"]
    end

  end

end
