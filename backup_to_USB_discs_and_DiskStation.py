#! /usr/bin/env python                                                                                                 
import os
import subprocess
import time

######## Settings
# Ask the user to execute?
prompt_flag = True

# Local directory
local_path = '/Users/[username]'
local_dirs = ['Desktop', 'Documents', 'Downloads', 'Dropbox', 'Movies', 'Music', 'Pictures']

# Backup drives 3-2-1 directories
drive1_dir = '/Volumes/disc_1'
drive2_dir = '/Volumes/disc_2'
drive3_dir = '/Volumes/disc_3'
drive_dirs = ['BACKUP', 'MANUAL']

# DiskStation directory
ds_server = '[NAS_IP]'
ds_dir = '[user]@' + ds_server + ':/var/services/homes/[user]'

# Define command to be used                                                                                          
command = 'rsync -avzh --update --delete --progress {src} "{dest}"'




def quotes(text):
    return '"' + str(text) + '" '

def get_local_sources(local_path, local_dirs):
    local_source = ''
    for entry in local_dirs:
        local_source += quotes(os.path.join(local_path, entry))
        local_source += ' '
    return local_source[:-1]

def transfers_local_drive(local_path, local_dirs, drive_dir):
    return [{'src':get_local_sources(local_path, local_dirs), 'dest':os.path.join(drive_dir,'BACKUP')}]

def transfers_local_ds(local_path, local_dirs, ds_dir):
    return [{'src':get_local_sources(local_path, local_dirs), 'dest':os.path.join(ds_dir,'BACKUP')}]

def transfers_drive_drive(driveA_dir, drive_dirs, driveB_dir):
    return [{'src':get_local_sources(driveA_dir, drive_dirs), 'dest': driveB_dir}]

def transfers_ds_drive(ds_dir, drive_dir):
    return [{'src':quotes(os.path.join(ds_dir, 'MANUAL')), 'dest': drive_dir}]

def check_default_folders_exist(path, defaults):
    for folder in defaults:
        new_folder_path = os.path.join(path, folder)
        if os.path.isdir(path) and not os.path.isdir(new_folder_path):
            mkdir_command = 'mkdir "{dir_path}"'
            subprocess.call(mkdir_command.format(dir_path=new_folder_path), shell=True)
            print ('<STATUS> created: ' + new_folder_path)

def create_default_folders(drive1_dir, drive2_dir, drive3_dir, drive_dirs):
    check_default_folders_exist(drive1_dir, drive_dirs)
    check_default_folders_exist(drive2_dir, drive_dirs)
    check_default_folders_exist(drive3_dir, drive_dirs)

def check_connected_device_setup(local_path, drive1_dir, drive2_dir, drive3_dir):
    local = os.path.isdir(local_path)
    drive1 = os.path.isdir(drive1_dir)
    drive2 = os.path.isdir(drive2_dir)
    drive3 = os.path.isdir(drive3_dir)

    ds = False
    if prompt_user('Is DiskStation available? (This will back-up to it and will copy MANUAL from it to USB discs)    y/[n]: ', prompt_flag):
        ds = True

    # which scenario do we have?
    if local:
        print('<SETUP> Connected: Host laptop')
    if ds:
        print('<SETUP> Connected: DiskStation')
    if drive1:
        print('<SETUP> Connected: Drive1')
    if drive2:
        print('<SETUP> Connected: Drive2')
    if drive3:
        print('<SETUP> Connected: Drive3')

    return local, ds, drive1, drive2, drive3

def build_transfers(local, ds, drive1, drive2, drive3, local_dirs, ds_dir, drive1_dir, drive2_dir, drive3_dir):
    transfers = []

    # to transfer LOCAL files to BACKUP folder on DS
    if local and ds:
        transfers += transfers_local_ds(local_path, local_dirs, ds_dir)

    # to transfer MANUAL folder from DS to DRIVES
    if ds and drive1:
        transfers += transfers_ds_drive(ds_dir, drive1_dir)   
    if ds and drive2:
        transfers += transfers_ds_drive(ds_dir, drive2_dir)   
    if ds and drive3:
        transfers += transfers_ds_drive(ds_dir, drive3_dir)   

    # to transfer LOCAL files to BACKUP folder on DRIVES
    if local and drive1:
        transfers += transfers_local_drive(local_path, local_dirs, drive1_dir)
    if local and drive2:
        transfers += transfers_local_drive(local_path, local_dirs, drive2_dir)
    if local and drive3:
        transfers += transfers_local_drive(local_path, local_dirs, drive3_dir)

    # to sync MANUAL & BACKUP folders between DRIVES
    if drive1 and drive2:
        transfers += transfers_drive_drive(drive1_dir, drive_dirs, drive2_dir)
    if drive1 and drive3:
        transfers += transfers_drive_drive(drive1_dir, drive_dirs, drive3_dir)
    if drive2 and drive3:
        transfers += transfers_drive_drive(drive2_dir, drive_dirs, drive3_dir)

    return transfers

def validate_transfers(transfers):
    valid_transfers = []
    print_line('Validating transfers')
    for transfer in transfers:
        valid_transfers.append(transfer)
        print('<Transfer>')
        print('FROM: ' + transfer['src'])
        print('TO:   ' + transfer['dest'])
    print_line()
    print(' ')
    print(' ')
    return valid_transfers
        
def transfer(valid_transfers, command):
    print_line('Start transfers')
    for transfer in valid_transfers:
        print('<New Transfer>')
        src = transfer['src']
        dest = transfer['dest']
        #print(command.format(src=src, dest=dest)) 
        subprocess.call(command.format(src=src, dest=dest), shell=True)
    print_line()
    print(' ')
    print(' ')

def prompt_user(prompt, prompt_flag=True, positive=['y', 'Y', 'yes']):
    if not prompt_flag:
        return True

    if raw_input(prompt) in positive:
        return True
    else:
        return False

def print_line(text=''):
    print('---------------------------------- ' + text)

def main(command, prompt_flag, local_dirs, ds_dir, drive1_dir, drive2_dir, drive3_dir, drive_dirs):

    create_default_folders(drive1_dir, drive2_dir, drive3_dir, drive_dirs)
    local, ds, drive1, drive2, drive3 = check_connected_device_setup(local_path, drive1_dir, drive2_dir, drive3_dir)
    transfers = build_transfers(local, ds, drive1, drive2, drive3, local_dirs, ds_dir, drive1_dir, drive2_dir, drive3_dir)

    valid_transfers = validate_transfers(transfers)
    start_time = 0
    end_time = 0
    if len(valid_transfers) > 0:
        if prompt_user('Continue? y/[n]: ', prompt_flag):
            start_time = time.time()
            transfer(valid_transfers, command)
            end_time = time.time()

    run_time = end_time - start_time
    print('Run time: {}h:{}m:{}s'.format(int(run_time/3600),int(run_time/60)%60, int(run_time%60)))


######## Execute main
main(command, prompt_flag, local_dirs, ds_dir, drive1_dir, drive2_dir, drive3_dir, drive_dirs)
