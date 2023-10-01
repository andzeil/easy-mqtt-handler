#!/bin/bash
BOLD1=$(tput bold)
BOLD0=$(tput sgr0)

echo "easy MQTT handler - Translation template (POT) generator script - Copyright (C) 2023 A. Zeil"

if [ ! -f "./src/easy_mqtt_handler/__main__.py" ]; then
  echo "[-] This script is part of easy MQTT handler and shall only be run via ${BOLD1}make translation-templates${BOLD0} in the repos main directory. Exiting."
  echo "[*] If you really really still want to call it directly, please try this in the root directory of the repo:"
  echo "    ${BOLD1}./src/scripts/translation-generate-pots.sh${BOLD0}"
  exit 1
else
  echo [+] easy MQTT folder detected: "$(pwd)"
fi

echo "[*] Checking environment and dependencies ..."

if ! command -v pygettext3 &> /dev/null
then
    echo "[-] Dependency ${BOLD1}pygettext3${BOLD0} could not be found. Should be part of the ${BOLD1}python3${BOLD0} package."
    echo "[*] Please try to get some help online."
    exit 1
else
    echo "[+] Dependency ${BOLD1}pygettext3${BOLD0} found. Proceeding ..."
fi

PYFILES=$(find . -name "*.py" -not -path "*/.venv/*" -not -path "*/build/*" -not -path "*/dist/*" -not -name "__init__.py")
TOTRANSLATE=""

while IFS= read -r line; do
    MATCHED=$(grep -c "translate = gettext.translation" "$line")
    if [ "$MATCHED" -eq 1 ]; then
      echo "[*] Found source file to translate: ${BOLD1}$line${BOLD0}."
      TOTRANSLATE+=$line$'\n'
    fi
done <<< "$PYFILES"

echo

while IFS= read -r line; do
    # PYSPATH=$(echo ${line%/*})
    PYSNAME="${line##*/}"
    POSNAME="${PYSNAME%.*}".po

    POTHEADER="# easy MQTT handler - translation file - $POSNAME"$'\n'
    POTHEADER+="# SPDX-License-Identifier: GPL-3.0-or-later"$'\n'
    POTHEADER+="# Copyright (C) 2023 A. Zeil"$'\n'
    POTHEADER+=$'\n'
    POTHEADER+="#"$'\n'
    POTHEADER+="msgid \"\""$'\n'
    POTHEADER+="msgstr \"\""$'\n'
    POTHEADER+="\"POT-Creation-Date: $(date +"%F %H:%M%z")\\n\""$'\n'
    POTHEADER+="\"MIME-Version: 1.0\\n\""$'\n'
    POTHEADER+="\"Content-Type: text/plain; charset=UTF-8\\n\""$'\n'
    POTHEADER+="\"Content-Transfer-Encoding: 8bit\\n\""$'\n'
    POTHEADER+="\"Generated-By: pygettext.py 1.5\\n\""$'\n'
    POTHEADER+=$'\n'

    if [ "$PYSNAME" != "" ]; then
      POTFILE=./src/easy_mqtt_handler/locale/templates/${PYSNAME%.*}.pot
      TEMPCONTENT="$POTHEADER"$'\n'
      echo "[*] Generating template file ${BOLD1}$POTFILE${BOLD0}."

      if [[ "$(pygettext3 -p ./src/easy_mqtt_handler/locale/templates/ -d "${PYSNAME%.*}" "$line")" -eq 0 ]]; then
        echo "[+] Template file ${BOLD1}$POTFILE${BOLD0} generated ${BOLD1}successfully${BOLD0}."
      else
        echo "[-] Error generating template file ${BOLD1}$POTFILE${BOLD0}. Error code was: ${BOLD1}$?${BOLD0}."
        exit 1
      fi
      TEMPCONTENT+=$(tail -n $(($(wc -l < "$POTFILE")-17)) "$POTFILE")
      echo "$TEMPCONTENT" > "$POTFILE"
    fi
done <<< "$TOTRANSLATE"

echo
echo "[*] All done. ${BOLD1}Exiting.${BOLD0}"
exit 0
