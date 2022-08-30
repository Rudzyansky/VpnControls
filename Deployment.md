# Setup

## For runner

<details>
<summary>Oracle Linux 7</summary>

```
module exec_from_home_dir 1.0;

require {
        type user_home_t;
        type init_t;
        class file { create execute execute_no_trans ioctl lock open read write };
}

#============= init_t ==============

allow init_t user_home_t:file { create execute execute_no_trans ioctl lock open read write };
```

</details>


Creating user under root<br>
Other commands under user

## Create user

```shell
useradd -b /opt -s /sbin/nologin -mNr vpn-controls
```

## Clone repository

```shell
git clone https://github.com/Rudzyansky/VpnControls.git ~/src
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
sed -ie '/^root/s/$/\nvpn-controls ALL=NOPASSWD: /sbin/strongswan rereadsecrets/' /etc/sudoers
```

## Dependencies

```shell
pip3 install --user -U pip
pip3 install --user -r $HOME/src/requirements.txt
```

## Systemd

```shell
sed -e 's|^(User)=.*$|\1=vpn-controls|' ~/src/VpnControls.service > /etc/systemd/system/VpnControls.service
systemctl --now enable VpnControls.service
```

# Update

```shell
sudo systemctl stop VpnControls
git pull origin master
sudo systemctl start VpnControls
```
