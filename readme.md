The backup script will copy pre-defined folders from the host to a NAS (Synology) and/or to USB discs (3 different ones are possible at the moment) if attached.
Run the script with:

```
python backup_to_USB_discs_and_DiskStation.py
```

The backup will be placed in a folder called *BACKUP*. In addition, a folder called *MANUAL* exists on all backup media (NAS and 3x USB discs). This folder will backup in following sequence NAS>USB1>USB2>USB3.

For the special case where modifications to the *MANUAL* folder on USB1 have been made, use following script to sync the manual folder from USB1>NAS:
```
python backup_MANUAL_from_USB_DRIVE1_to_DiskStation.py
```

## Passwordless rsync

On the NAS the rsync service needs to be activated:
Control panel > File Services > rsync > Enable rsync service (do not check Enable rsync account).
For the designated user rysnc then also needs to be allowed (under User > Edit > Applications). 

Remember:
- By default, root is not allowed to connect, you need to connect with another user and use ```sudo -i``` (then type the password of the user you are connected with)
- Only members of the administrators group are allowed to connect by SSH. However, even non-administrators can use the rsync service.

### Enabling Public key authentification
This is disabled by default.
Add the designated user temporarily to the administrators group (Control panel > User > [user] > Edit > User groups).

SSH into the NAS:
```
ssh [user]@[nas-ip]
```
Change to root:
```
sudo -i
```
Edit the SSH service config:
```
vim /etc/ssh/sshd_config
```
(in vim, press 'i' for insert mode, 'ctrl + c' to quit insert mode, and ':' for command mode. ':wq' will write current changes and quit vim)

Uncomment the lines ```PubkeyAuthentication yes``` and ```AuthorizedKeysFile .ssh/authorized_keys``` (make sure not to change anything else, otherwise you could lock yourself out of SSH).

Restart the SSH service by disabling and re-enabling the SSH service in Control panel > Terminal & SNMP.

Logout of the NAS.
Check that the current laptop/pc (to connect to the NAS with) has a pair of SSH keys (in */.ssh*). If not, generate these with ```ssh-keygen -t rsa```.
If a key pair exists copy the relevant bits to the NAS with:
```
ssh-copy-id [user]@[nas-ip]
```
Now connect to the NAS again with SSH and that user (```ssh [user]@[nas-ip]```), and change following file permissions:
```
chmod 0711 ~
chmod 0711 ~/.ssh
chmod 0600 ~/.ssh/authorized_keys
```
Exit. Now passwordless SSH should work. Remove the user from the administrator group and disable SSH access again. Now passwordless rsync should remain working! 


Based on this [tutorial](https://silica.io/using-ssh-key-authentification-on-a-synology-nas-for-remote-rsync-backups/).