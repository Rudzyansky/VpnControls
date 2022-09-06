# Setup

```shell
# Oracle Linux 7 setup python
yum -y install python39{,-pip,-setuptools}
alternatives --set python3 /usr/bin/python3.9
ln -s /bin/pip{3,}

# Create user for pipeline
useradd -mNrs /sbin/nologin runner

# Create user for app
useradd -mNrs /sbin/nologin tgbot

# Sudo permissions setup
sed -e '/^root/s|$|\n'\
'tgbot\tALL=NOPASSWD:\t/sbin/strongswan stroke rereadsecrets\n'\
'runner\tALL=NOPASSWD:\t/home/runner/actions-runner/svc.sh, \\\n'\
'\t\t\t/bin/rm -rf /usr/src/tgbot, \\\n'\
'\t\t\t/bin/cp -Rf . /usr/src/tgbot, \\\n'\
'\t\t\t/bin/systemctl stop VpnControls, \\\n'\
'\t\t\t/bin/systemctl start VpnControls'\
'|' -i /etc/sudoers

# Follow instructions: https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners

# Enable and start runner service
sudo -u runner sh -c 'cd ~/actions-runner; sudo ./svc.sh install; sudo ./svc.sh start; sudo ./svc.sh status'

# Run deploy action (merge PR to master)

# Install dependencies
sudo -u tgbot sh -c 'pip install --user -U pip; pip install --user -r /usr/src/tgbot/requirements.txt'

# strongSwan configure
echo 'include users/ipsec.*.secrets' >> /etc/strongswan/ipsec.secrets

# Create directory for store credentials
sh -c 'cd /etc/strongswan; mkdir users; chown tgbot:root users; chmod 750 users'

# Environment file setup
sed -re 's|^^^^^^^^^(ADDRESS)=.*$|\1=vpn.example.com|' \
    -re 's|^^^^^^^^^^(API_ID)=.*$|\1=000000|' \
    -re 's|^^^^^^^^(API_HASH)=.*$|\1=ffffffffffffffffffffffffffffffff|' \
    -re 's|^^^^^^^^^^^(TOKEN)=.*$|\1=0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|' \
    -re 's|^(SECRETS_PATTERN)=.*$|\1=/etc/strongswan/users/ipsec.%s.secrets|' \
/usr/src/tgbot/template.env > /home/tgbot/.env

# Systemd service setup
sed -re 's|^(User)=.*$|\1=tgbot|' \
    -re 's|^(EnvironmentFile)=.*$|\1=/home/tgbot/.env|' \
/usr/src/tgbot/VpnControls.service > /etc/systemd/system/VpnControls.service

# Systemd service enable and start
systemctl --now enable VpnControls.service
```

# Troubleshooting

## Access denied

```shell
yum install policycoreutils-python-utils  # audit2allow (Oracle Linux 7)
PACKAGE_NAME="actions_runner"
semodule -DB && setenforce permissive
sudo -u runner sh -c 'cd ~/actions-runner; sudo ./svc.sh start; sudo ./svc.sh stop'
audit2allow -M "$PACKAGE_NAME" -b
setenforce enforcing && semodule -B
# vim "$PACKAGE_NAME".te
# checkmodule -M -m -o "$PACKAGE_NAME".mod "$PACKAGE_NAME".te && \
# semodule_package -o "$PACKAGE_NAME".pp -m "$PACKAGE_NAME".mod && \
semodule -i "$PACKAGE_NAME".pp
```