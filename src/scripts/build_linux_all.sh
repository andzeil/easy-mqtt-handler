#! /bin/bash
BOLD1=$(tput bold)
BOLD0=$(tput sgr0)

echo "easy MQTT handler - mass linux package building script - Copyright (C) 2023 A. Zeil"

if [ ! -f "./src/easy_mqtt_handler/__main__.py" ]; then
  echo "[-] This script is part of easy MQTT handler and shall only be run via ${BOLD1}make build-all-linux${BOLD0} in the repos main directory. Exiting."
  echo "[*] If you really really still want to call it directly, please try this in the root directory of the repo:"
  echo "    ${BOLD1}./src/scripts/build_linux_all.sh${BOLD0}"
  exit 1
fi

. .venv/bin/activate

# briefcase package

briefcase package --target archlinux:latest

briefcase package --target debian:11
briefcase package --target debian:12

briefcase package --target ubuntu:18.04
briefcase package --target ubuntu:20.04
briefcase package --target ubuntu:22.04


briefcase package --target fedora:36
briefcase package --target fedora:37
briefcase package --target fedora:38

briefcase package --target almalinux:7
briefcase package --target almalinux:8
briefcase package --target almalinux:9

exit 0
