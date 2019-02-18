#!/bin/bash
shopt -s extglob

# Prepare for possible custom user
if [ "/home/$NB_USER" != "/home/jovyan" ]; then
    if [ -d "/home/jovyan" ]; then
        cp -R /home/jovyan /home/$NB_USER
        rm -r /home/jovyan
    fi
fi

# Ensure correct permissions
mkdir -p /home/$NB_USER/{erda_mount,slurm_mount}
chown -R $NB_UID:$NB_GID /home/$NB_USER/.[^.]*
chown -R $NB_UID:$NB_GID /home/$NB_USER/!(slurm_mount)