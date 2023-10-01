#!/bin/bash
BOLD1=$(tput bold)
BOLD0=$(tput sgr0)

echo "easy MQTT handler - Translation file (MO) generator script - Copyright (C) 2023 A. Zeil"

if [ ! -f "./src/easy_mqtt_handler/__main__.py" ]; then
  echo "[-] This script is part of easy MQTT handler and shall only be run via ${BOLD1}make compile-translations${BOLD0} in the repos main directory. Exiting."
  echo "[*] If you really really still want to call it directly, please try this in the root directory of the repo:"
  echo "    ${BOLD1}./src/scripts/translation-compile-mos.sh${BOLD0}"
else
  echo [+] easy MQTT folder detected: "$(pwd)"
fi

echo "[*] Checking environment and dependencies ..."

if ! command -v msgfmt &> /dev/null
then
    echo "[-] Dependency ${BOLD1}msgfmt${BOLD0} could not be found. Should be part of the ${BOLD1}gettext${BOLD0} package."
    echo "[*] Please try to get some help online."
    exit 1
else
    echo "[+] Dependency ${BOLD1}msgfmt${BOLD0} found. Proceeding ..."
fi

POFILES=$(find . -name "*.po" -not -path "*/.venv/*" -not -path "*/build/*" -not -path "*/dist/*")

while IFS= read -r line; do
    POSPATH=${line%/*}
    POSNAME=${line##*/}
    MOSNAME="${POSNAME%.*}".mo

    if [[ "$(msgfmt -o "$POSPATH/$MOSNAME" "$line")" -eq 0 ]]; then
      echo "[+] PO file ${BOLD1}$line successfully${BOLD0} compiled."
      echo "[+] New .mo  file is: ${BOLD1}$POSPATH/$MOSNAME${BOLD0}."
    else
      echo "[-] Error compiling .po file ${BOLD1}$line${BOLD0}. Error code was: ${BOLD1}$?${BOLD0}."
      exit 1
    fi
  echo
done <<< "$POFILES"

echo

echo "[+] All done. ${BOLD1}Exiting.${BOLD0}"
exit 0
