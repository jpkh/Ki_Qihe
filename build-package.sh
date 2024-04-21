#!/bin/sh
##########################################################
#
# Script: build-package.sh
# Author: Jani Hirvinen, <jani@jdronics.fi>
# Date: 2024-04-07
# Version: 1.0
#
# Description: Build script for KiCad QiHe plugin
#
# Works:
#  - Windows/Cywin
#  - Linux
#  - MacOS
#

# Define the source directory for the plugin
plugin_dir="qihe"
config_file="${plugin_dir}/config.py"

# Extract version and date from the config.py file
def_version=$(grep 'def_version' $config_file | cut -d "=" -f 2 | tr -d " \r'\"")
def_date=$(grep 'def_date' $config_file | cut -d "=" -f 2 | tr -d " \r'\"")

# Remove possible - from the date value
def_date=$(echo $def_date | tr -d '-')

# Print extracted values (for debugging)
echo "Version: $def_version"
echo "Date: $def_date"

# Remove old build directory
rm -rf build # remove old build directory

# Create new build directory
mkdir -p build/resources build/plugins

# Copy files to build directory
cp metadata.json build

# Copy plugin files to build directory
cp qihe/* build/plugins

# Copy icon to build directory
cp -r qihe/icon*.png build/resources/icon.png

# Change to build directory and create zip package of the plugin
cd build && zip -r ../ki-qihe-v${def_version}-${def_date}.zip *

