#! /bin/bash
BOLD1=$(tput bold)
BOLD0=$(tput sgr0)

echo "easy MQTT handler - Icons regenerator script - Copyright (C) 2023 A. Zeil"

if [ ! -f "./src/easy_mqtt_handler/__main__.py" ]; then
  echo "[-] This script is part of easy MQTT handler and shall only be run via ${BOLD1}make regenerate-icons${BOLD0} in the repos main directory. Exiting."
  echo "[*] If you really really still want to call it directly, please try this in the root directory of the repo:"
  echo "    ${BOLD1}./src/scripts/regenerate_icon_files.sh${BOLD0}"
  exit 1
else
  echo [+] easy MQTT folder detected: "$(pwd)"
fi

echo "[*] Checking environment and dependencies ..."

if ! command -v inkscape &> /dev/null
then
    echo "[-] Dependency ${BOLD1}inkscape${BOLD0} could not be found. Please install it using your package manager of choice or try to get some help online."
    exit 1
else
    echo "[+] Dependency ${BOLD1}inkscape${BOLD0} found. Proceeding ..."
fi

if ! command -v convert &> /dev/null
then
    echo "[-] Dependency ${BOLD1}imagemagick${BOLD0} could not be found. Please install it using your package manager of choice or try to get some help online."
    exit 1
else
    echo "[+] Dependency ${BOLD1}imagemagick${BOLD0} found. Proceeding ..."
fi

if ! command -v png2icns &> /dev/null
then
    echo "[-] Dependency ${BOLD1}icnsutils${BOLD0} could not be found. Please install it using your package manager of choice or try to get some help online."
    exit 1
else
    echo "[+] Dependency ${BOLD1}icnsutils${BOLD0} found. Proceeding ..."
fi

ICON_PATH="src/easy_mqtt_handler/assets/app-icon"

# delete old icons
echo "[-] Deleting old icon files ..."
rm -f "${ICON_PATH}/app-icon-*.png"
rm -f "${ICON_PATH}/app-icon.ico"
rm -f "${ICON_PATH}/app-icon.icns"

# linux - PNGs
echo "[+] Creating new icon files for Linux"
inkscape -w 16 -h 16 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-16.png"
inkscape -w 32 -h 32 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-32.png"
inkscape -w 48 -h 48 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-48.png"
inkscape -w 64 -h 64 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-64.png"
inkscape -w 128 -h 128 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-128.png"
inkscape -w 256 -h 256 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-256.png"
inkscape -w 512 -h 512 "${ICON_PATH}/app-icon.svg" -o "${ICON_PATH}/app-icon-512.png"

# windows - ICO
echo "[+] Creating new icon file for Windows"
convert -transparent white "${ICON_PATH}/app-icon-16.png" "${ICON_PATH}/app-icon-32.png" "${ICON_PATH}/app-icon-48.png" "${ICON_PATH}/app-icon-64.png" "${ICON_PATH}/app-icon.ico"

# macOS - ICNS
echo "[+] Creating new icon file for MacOS"
png2icns "${ICON_PATH}/app-icon.icns" "${ICON_PATH}/app-icon-16.png" "${ICON_PATH}/app-icon-32.png" "${ICON_PATH}/app-icon-48.png" "${ICON_PATH}/app-icon-128.png" "${ICON_PATH}/app-icon-256.png" "${ICON_PATH}/app-icon-512.png"

echo "[*] Done. Exiting."
exit 0
