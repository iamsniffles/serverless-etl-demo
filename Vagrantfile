# -*- mode: ruby -*-
# vi: set ft=ruby :

# YOUR AWS ACCOUNT INFORMATION
AWSID = ''
REG = ''
AWS_KEY = ''
AWS_SECRET = ''
S3BUCKET = ''
DBURL = ''
API_KEY = ''

# YOUR VM TIMEZONE
TZONE = 'Asia/Jakarta'

Vagrant.configure('2') do |config|
  config.vm.box = 'bento/ubuntu-16.04'

  $script = <<-SCRIPT
  sudo apt-get update
  sudo timedatectl set-timezone #{TZONE}
  sudo timedatectl set-ntp no
  sudo apt-get install ntp
  curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
  echo 'export PATH="~/.pyenv/bin:$PATH"' >> /home/vagrant/.bash_profile
  echo 'eval "$(pyenv init -)"' >> /home/vagrant/.bash_profile
  echo 'eval "$(pyenv virtualenv-init -)"' >> /home/vagrant/.bash_profile
  echo 'export API_KEY=#{API_KEY}' >> /home/vagrant/.bash_profile
  echo 'export DBURL=#{DBURL}' >> /home/vagrant/.bash_profile
  echo 'export AWSID=#{AWSID}' >> /home/vagrant/.bash_profile
  echo 'export S3BUCKET=#{S3BUCKET}' >> /home/vagrant/.bash_profile
  echo 'export REG=#{REG}' >> /home/vagrant/.bash_profile
  source ~/.bash_profile
  sudo apt-get update
  sudo apt-get -y install libbz2-dev libsqlite3-dev
  pyenv install 3.6.2
  pyenv global 3.6.2
  pip install flatten_json dataset s3fs
  curl -sL https://deb.nodesource.com/setup_7.x | sudo bash
  sudo apt-get install nodejs
  cd /vagrant
  sudo npm install -g serverless
  sudo npm init -y
  sudo npm install --save serverless-step-functions
  sudo npm install --save serverless-python-requirements
  serverless config credentials --provider aws --stage dev --key #{AWS_KEY} --secret #{AWS_SECRET}
  SCRIPT

  config.vm.provision 'shell', inline: $script, privileged: false
end
