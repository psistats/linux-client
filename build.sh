#!/bin/bash

rm -rf dist deb_dist

./build-src.sh
./build-debian.sh
