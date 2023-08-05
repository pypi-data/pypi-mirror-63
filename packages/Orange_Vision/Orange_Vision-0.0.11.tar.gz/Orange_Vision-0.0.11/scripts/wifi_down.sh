sudo sed -i '/hosts/c\hosts:          files mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns myhostname' /etc/nsswitch.conf
sudo sed -i '/AVAHI_DAEMON_DETECT_LOCAL/c\AVAHI_DAEMON_DETECT_LOCAL=0' /etc/default/avahi-daemon
sudo service avahi-daemon restart