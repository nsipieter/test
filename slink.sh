#!/bin/bash

SRC="/home/wpain/Bureau/hypervision/sources"
CPS="/opt/canopsis"

#cd $SRC/webcore-libs/var/www/canopsis/resources/lib
#sudo rm -R jqGridable
#ln -s /home/wpain/Bureau/gittmp/jqGridable jqGridable
#cd -

#cd ../sources
rm $SRC/webcore/var/www/canopsis/resources/lib
ln -s $SRC/externals/webcore-libs $SRC/webcore/var/www/canopsis/resources/lib

sudo rm -R $CPS/opt/webcore
sudo ln -s $SRC/webcore/opt/webcore $CPS/opt/

sudo rm -Rf $CPS/var/www/canopsis
sudo ln -s $SRC/webcore/var/www/canopsis $CPS/var/www/


sudo rm -R $CPS/lib/canolibs
sudo ln -s $SRC/canolibs/lib/canolibs $CPS/lib/

sudo rm -R $CPS/opt/snmp2amqp
sudo ln -s $SRC/snmp2amqp/opt/snmp2amqp $CPS/opt/
sudo rm -R $CPS/var/snmp
sudo ln -s $SRC/snmp2amqp/var/snmp $CPS/var/

sudo rm -R $CPS/opt/collectd-libs
sudo ln -s $SRC/collectd-libs/opt/collectd-libs $CPS/opt/

sudo rm -R $CPS/opt/amqp2engines
sudo ln -s $SRC/amqp2engines/opt/amqp2engines $CPS/opt/

sudo rm -R $CPS/opt/mongodb
sudo ln -s $SRC/mongodb-conf/opt/mongodb $CPS/opt/