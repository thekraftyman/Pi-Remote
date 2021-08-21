#!/bin/sh

# update
sudo apt update

# install packages
sudo apt install -y python3 python3-dev python3-pip gcc

# install python libraries
pip3 install -r requirements.txt

# make the dir on the pi for our script
mkdir /home/pi/scripts

# copy our power scripts over to the scripts folder
cp power_on_off.py /home/pi/scripts/power_on_off.py

# Tell the installer to run this in the rc.local file
echo "In order to run this script, you must add this line in the /etc/rc.local file (before the exit):"
cat <<EOF
sudo python3 /home/pi/scripts/power_on_off.py &
EOF
