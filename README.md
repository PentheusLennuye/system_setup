# Ubuntu Setup

This playbook structure installs what I need on Ubuntu servers and workstations
according to what I would like.

## Installing everything

1. Ensure that sudo is installed and the current user has sudo rights. Update
   the system and reboot.
  ```sh
  su -
  TGTUSER=<username>
  echo "$TGTUSER ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/$TGTUSER
  chmod 600 /etc/sudoers.d/$TGTUSER
  apt-get update
  apt-get install -y sudo
  apt-get upgrade
  ```

2. Install ansible and fire away. Get coffee, TeX takes a long time...
  ```sh
  sudo apt-get install -y ansible
  ansible-galaxy collection install community.general
  ansible-playbook site.yml
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
