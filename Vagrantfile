# -*- mode: ruby -*-
# vi: set ft=ruby ts=2 sw=2 expandtab :

PROJECT = "line_report_generator"
LINE_REPORT_GENERATOR_PORT = 8989
DB_USER = "vagrant"
DB_PASSWORD = "vagrant"
DB_HOST = "db"
DB_NAME = "vagrant"

LINE_BOT_CHANNEL_ACCESS_TOKEN = "xxxx"
LINE_BOT_CHANNEL_SECRET = "xxxx"

# to avoid typing --provider docker --no-parallel
# at every vagrant up
ENV['VAGRANT_NO_PARALLEL'] = 'yes'
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'
VAGRANTFILE_VERSION = "2"
Vagrant.configure(VAGRANTFILE_VERSION) do |config|

  config.vm.define "db" do |db|
    db.vm.provider "docker" do |d|
      d.image = "postgres:9.6"
      d.name = "#{PROJECT}_db"
      d.env = {
          "POSTGRES_PASSWORD" => DB_PASSWORD,
          "POSTGRES_USER" => DB_USER,
          "POSTGRES_DB" => DB_NAME
      }
    end
  end

  environment_variables = {
      "HOST_USER_UID" => Process.euid,
      "TARGET" => "dev",
      "ENV_NAME" => "devdocker",
      "APP_PATH" => "/vagrant",
      "VIRTUAL_ENV_PATH" => "/tmp/virtual_env3",
      "LINE_REPORT_GENERATOR_PORT" => LINE_REPORT_GENERATOR_PORT,
      "LINE_BOT_CHANNEL_ACCESS_TOKEN" => LINE_BOT_CHANNEL_ACCESS_TOKEN,
      "LINE_BOT_CHANNEL_SECRET" => LINE_BOT_CHANNEL_SECRET,
      "DB_USER" => DB_USER,
      "DB_PASSWORD" => DB_PASSWORD,
      "DB_HOST" => DB_HOST,
      "DB_NAME" => DB_NAME
  }

  config.ssh.insert_key = true
  config.vm.define "dev", primary: true do |app|
    app.vm.provider "docker" do |d|
      d.image = "alexzhxin/python-dev"
      d.name = "#{PROJECT}_dev"
      d.link "#{PROJECT}_db:#{DB_HOST}"
      d.has_ssh = true
      d.env = environment_variables
    end
    app.ssh.username = "vagrant"

    app.vm.provision "remove-old-key-file", type: "shell" do |s|
      s.inline = "
        rm -f /home/vagrant/.ssh/id_rsa
        "
    end

    # so that we can git clone from within the docker
    app.vm.provision "file", source: "~/.ssh/id_rsa", destination: ".ssh/id_rsa"
    # so that we can git push from inside the docker
    app.vm.provision "file", source: "~/.gitconfig", destination: ".gitconfig"

    # we can't copy in /root using file provisionner
    # hence the usage of shell
    app.vm.provision "permits-root-to-clone", type: "shell" do |s|
      s.inline = "
        cp /home/vagrant/.ssh/id_rsa ~/.ssh/id_rsa
        ssh-keyscan -H github.com >> $HOME/.ssh/known_hosts
        chmod 400 ~/.ssh/id_rsa
        "
    end

    app.vm.provision "ansible", type: "shell" do |ansible|
      ansible.env = environment_variables
      ansible.inline = "
          set -e
          cd $APP_PATH
          ssh-keyscan -H github.com >> $HOME/.ssh/known_hosts
          ansible-playbook build_scripts/ansible/bootstrap-dev.yml
          echo 'done, you can now run `vagrant ssh`'
        "
    end
  end
end
