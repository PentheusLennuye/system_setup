# Ubuntu Setup

This playbook structure installs what I need on Ubuntu servers and workstations
according to what I would like.

## Installing everything

1. Ensure that the current user has sudo rights.
  ```sh
  # file: /etc/sudoers.d/<username> with mod 0440
  <username> ALL=(ALL:ALL) NOPASSWD:ALL
  ```
2. Ensure the system is fully updated.
  ```sh
  sudo apt-get update
  sudo apt-get upgrade
  sudo reboot
  ```

3. Install ansible and fire away. Get coffee, TeX takes a long time...
  ```sh
  sudo apt-get install ansible
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
