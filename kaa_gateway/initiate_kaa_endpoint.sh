#!/bin/bash
APP_TAR_FILE_PATH=$1
DEVICES_DIR=$2
DEVICE_NAME=$3

DEVICE_DIR=$DEVICES_DIR/$DEVICE_NAME
sudo mkdir $DEVICE_DIR
sudo tar xf $APP_TAR_FILE_PATH -C $DEVICE_DIR
mkdir $DEVICE_DIR/$DEVICE_NAME
cd $DEVICE_DIR/$DEVICE_NAME
cmake -DKAA_MAX_LOG_LEVEL=3 ..
make