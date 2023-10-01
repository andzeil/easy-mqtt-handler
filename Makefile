# easy MQTT handler Makefile - Copyright (C) 2023 A. Zeil
NAME=easy_mqtt_handler

# Target to activate venv and install required python libs
activate-venv:
		python3 -m venv .venv; \
		. .venv/bin/activate; \
		./.venv/bin/pip install -r requirements.txt

# Target for housekeeping
clean:
	rm -rf build/ dist/ logs/ .venv/ src/$(NAME).dist-info/ src/$(NAME)/__pycache__ src/$(NAME)/locale/templates
	find -depth -type d -name "__pycache__" -exec rm -rf {} \;
	find -type f -name "*.mo" -exec rm {} \;

# Translation related targets
translation-templates:
		mkdir -p ./src/easy_mqtt_handler/locale/templates/
		./src/scripts/translation-generate-pots.sh

compile-translations:
		./src/scripts/translation-compile-mos.sh

# Target to regenerate icons - only needed if application icon was changed
regenerate-icons:
		./src/scripts/regenerate_icon_files.sh

# Target to create a Linux package for the distribution running on the current machine
package: activate-venv
	briefcase package

# Target to build packages for a lot of different Linux distributions
build-all-linux: activate-venv
	./src/scripts/build_linux_all.sh

# Target to create an AppImage for Linux
build-linux-appimage: activate-venv
	briefcase build linux appimage

# Target to build the MacOS app
build-macos-app: activate-venv
	briefcase build macos app

