The backup script will copy pre-defined folders from the host to a NAS (Synology) and/or to USB discs (3 different ones are possible at the moment) if attached.
Run the script with:

```
python backup_to_USB_discs_and_DiskStation.py
```

The backup will be placed in a folder called *BACKUP*. In addition, a folder called *MANUAL* exists on all backup media (NAS and 3x USB discs). This folder will be backup in following sequence NAS>USB1>USB2>USB3.

For the special case where modifications to the *MANUAL* folder on USB1 have been made, use following script to sync the manual folder from USB->NAS:
```
python backup_MANUAL_from_USB_DRIVE1_to_DiskStation.py
```

## Passwordless rsync

On the NAS the rsync service needs to be activated:
Control panel > File Services > rsync > Enable rsync service (do not check Enable rsync account).

For the designated user rysnc then also needs to be allowed (under User > Edit > Applications). 


....
https://silica.io/using-ssh-key-authentification-on-a-synology-nas-for-remote-rsync-backups/
....

To make sync passwordless for user XYZ, follow these steps:
- Mak XYZ part of the local administrator group.
- do this


Login into synology over ssh (enable it first) with a local administrator account.
change to root user with
```
sudo -i
```
mkdir /root/.ssh
cd /root/.ssh
ssh-keygen

(press enter for all questions)

At the end there is a private and public key file in /root/.ssh
the default key file names are id-rsa and id-rsa.pub


