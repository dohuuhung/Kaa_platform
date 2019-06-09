# Prepare directory
sudo mkdir -p /var/lib/kaa_gateway/applications
sudo mkdir -p /var/lib/kaa_gateway/devices

# Install dependence package
sudo pip install -r requirement.txt

# Preconfigure
- create config file /etc/kaa/kaa_gateway.conf with following content and modify corresponding your environment:
[DEFAULT]
kaa_gateway_addr=localhost
kaa_gateway_port=3004
kaa_server_addr=52.15.81.21
kaa_server_port=8080
mongodb_addr=localhost
mongodb_port=27017
kaa_database_name=kaa
kaa_gateway_db_name=kaa_gateway
kaa_admin_username=kaa
kaa_admin_user_password=kaa123
default_tenant_admin_user=admin
default_tenant_admin_pass=admin123
gen_token_key=xe3454g32

# Install sqlite3
sudo add-apt-repository ppa:jonathonf/backports
sudo apt-get update && sudo apt-get install sqlite3

# Create service in system
- create file /etc/systemd/system/kaa_gateway.service with following content:
[Unit]
Description = Kaa kaa_gateway.service

[Service]
ExecStart = <kaa_gateway_dir>/kaa_gateway.sh
User = root

[Install]
WantedBy = multi-user.target

- Then run following commands:
$ sudo systemctl start kaa_gateway.service
$ sudo systemctl enable kaa_gateway.service
$ sudo systemctl status kaa_gateway.service
