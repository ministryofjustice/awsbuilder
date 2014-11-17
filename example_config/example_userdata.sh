#cloud-config
repo_update: true
repo_upgrade: all

packages:
 - python-software-properties
 - python-support
 - git
 - python-pip
 - build-essential
 - python-dev
 - swig
 - libssl-dev


runcmd:
 - add-apt-repository -y ppa:saltstack/salt
 - pip install salt==0.17.4
 - pip install virtualenvwrapper
