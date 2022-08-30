#!/bin/bash

# install colon
if ! command -v colcon &> /dev/null
then
      sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
      sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
      sudo apt update
      sudo apt install python3-colcon-common-extensions -y
    exit
fi

# install torch
# install torch
var="$(lsb_release -sr)"
if [ $var = "18.04" ]; then
    # pip install torch torchvision  future
    pip2 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
    sudo apt-get install python-numpy
    python -m pip install --upgrade Pillow
    pip install -U PyYAML

fi

if [ $var = "20.04" ]; then
    pip3 install torch torchvision  future
    sudo apt-get install python3-numpy
    python3 -m pip install --upgrade Pillow
    pip3 install -U PyYAML

fi

echo "export VEHICLE_NAME=''" >> ~/.bashrc

# update cmake   

currentver=$(cmake --version | head -1 | cut -d' ' -f3)
echo $currentver
# need to makesure cmake is greater than version 3.13
requiredver="3.13.0"
if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
        echo "Greater than or equal to ${requiredver}"
else
   sudo apt update && \
   sudo apt install -y software-properties-common lsb-release && \
   sudo apt clean all
   wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
   sudo apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
   sudo apt update
   sudo apt install kitware-archive-keyring
   sudo rm /etc/apt/trusted.gpg.d/kitware.gpg
   sudo apt update
   sudo apt install cmake -y
fi
