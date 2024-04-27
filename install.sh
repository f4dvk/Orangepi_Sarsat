#!/bin/bash

apt-get update
apt-get -y upgrade

apt-get -y install git cmake libusb-1.0-0-dev
apt-get -y install python3-pip
pip3 install -U pywebio

apt-get -y install nginx-light   # accès web

echo
echo "-----------------------------------------------"
echo "----- Installing RTL-SDR Drivers and Apps -----"
echo "-----------------------------------------------"
cd /root
wget https://github.com/f4dvk/rtl-sdr/archive/master.zip
unzip master.zip
mv rtl-sdr-master rtl-sdr
rm master.zip

# Compile and install rtl-sdr
cd rtl-sdr/ && mkdir build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
make && make install && ldconfig
bash -c 'echo -e "\n# for RTL-SDR:\nblacklist dvb_usb_rtl28xxu\n" >> /etc/modprobe.d/blacklist.conf'
cd /root

wget https://github.com/f4dvk/Orangepi_Sarsat/archive/master.zip

unzip -o master.zip
mv Orangepi_Sarsat-master Orangepi_Sarsat
rm master.zip

cd /root/406

bash ./install.sh
