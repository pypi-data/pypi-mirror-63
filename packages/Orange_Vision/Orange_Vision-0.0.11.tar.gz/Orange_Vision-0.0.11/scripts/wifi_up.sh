sudo sed -i '/hosts/c\hosts:          files mdns4_minimal [NOTFOUND=return] dns' /etc/nsswitch.conf
sudo service avahi-daemon restart