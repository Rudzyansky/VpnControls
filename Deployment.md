# Setup

Creating user under root<br>
Other commands under user

## Create user

```shell
useradd -b /opt/vpn-controls -s /usr/bin/bash -mNr vpn-controls
```

#### Create ssh files

```shell
sudo -u vpn-controls mkdir ~/.ssh
sudo -u vpn-controls touch ~/.ssh/authorized_keys
sudo -u vpn-controls chmod 700 ~/.ssh
sudo -u vpn-controls chmod 600 ~/.ssh/authorized_keys
```

#### Generate ssh key

```shell
ssh-keygen -f /tmp/pipeline.key -b 4096 -C pipeline
cat /tmp/pipeline.key.pub >> /opt/vpn-controls/.ssh/authorized_keys
cat /tmp/pipeline.key
rm -f /tmp/pipeline.key{,.pub}
```

## Clone repository

```shell
git clone git@github.com:Rudzyansky/VpnControls.git ~/src
```

## Environment file setup

### sed way

```shell
sed -re 's|^^(ADDRESS)=.*$|\1=vpn.example.com|' \
    -re 's|^^^(API_ID)=.*$|\1=000000|' \
    -re 's|^(API_HASH)=.*$|\1=ffffffffffffffffffffffffffffffff|' \
    -re 's|^^^^(TOKEN)=.*$|\1=0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|' \
~/src/template.env > ~/.env
```

### vim way

```shell
cp ~/{src/template.env,.env}
vim ~/.env
```

## Directories and Permissions

```shell
mkdir $HOME/users
chmod 600 $HOME/.env
chmod 750 $HOME{,/users}
chgrp root $HOME{,/users}
sed -ie '/^root/s/$/\nvpn-controls ALL = NOPASSWD: strongswan rereadsecrets/' /etc/sudoers
```

## Dependencies

```shell
pip install --user $HOME/src/requirements.txt
```

## Systemd

```shell
systemctl --user --now enable $HOME/src/VpnControls.service
```

# Update

```shell
systemctl --user stop VpnControls
git pull origin master
systemctl --user start VpnControls
```
