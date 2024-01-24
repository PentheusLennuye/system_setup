# Ubuntu Setup

This playbook structure installs what I need on Ubuntu servers and workstations
according to what I would like.

## Networking?

If the workstation acts as a server, then edit _/etc/network/interfaces/_ and
replace 'inet dhcp' with 'inet static' for the given interface and add the 
static info. Example:

```text
iface wlx107b44eb4fb3 inet static
    address 192.168.68.33/24
    gateway 192.168.68.1
```

Don't forget to change /etc/resolv.conf as well.

## Set up the Client

1. Ensure that sudo is installed and the current user has sudo rights. Update
   the system and reboot.
  ```sh
  su -
  apt-get update
  apt-get install -y sudo
  U=<username>
  echo "$U ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/$U
  chmod 600 /etc/sudoers.d/$U
  apt-get upgrade
  reboot
  ```

## Set up the Ansible Host

2. Install ansible and fire away. Get coffee, TeX takes a long time...
  ```sh
  sudo apt-get install -y ansible
  ansible-galaxy collection install community.general community.postgresql
  ansible-playbook site.yml
  ```

## nVidia on Debian

1. In _/etc/apt/sources.list_, alter the first 'deb' line to read:

  ```text
  deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
  ```

2. Update and then install nvidia non free with `apt-get install nvidia-driver
   firmware-misc-nonfree`

## Flatpak

```bash
sudo flatpak remote-add --if-not-exists flathub \
https://dl.flathub.org/repo/flathub.flatpakrepo

sudo flatpak install flatpak sh.cider.Cider
sudo flatpak install flatpak net.cozic.joplin_desktop
```

## Creating a new role

```sh
ROLENAME=<role name>
SUBDIRS=(tasks handlers templates files vars defaults meta library \
         module_utils lookup_plugins)
for sd in $SUBDIRS; do
  mkdir -p roles/$ROLENAME/$sd
  touch roles/$ROLENAME/$sd/.keep
done
echo "---\n- name: name me\n  become: yes\n  ansible.builtin.xxx: yyy" > \
roles/$ROLENAME/tasks/main.yml
```

## Visual Studio Code Setup (for Desktop Environments)

### Install the following extensions

- C/C++
- C/C++ Extension Pack
- Go
- markdownlint
- Monokai Pro (needs licence)
- Remote Development (installs Tunnel, SSH, SSH Editing, Dev Containers)
- Rewrap
- Python
- Vim
- vscode-pdf

### Set the lines

1. _File > Preferences > Settings_
2. _Text Editor > Rulers > settings.json_
3. __"editor.rulers": [80, 120]__
4. Save
