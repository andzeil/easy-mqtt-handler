# Structure of the repository

The repository is structured in a way that should help you to navigate it.

Inside the root directory you will find all the needed files for the build system, the License and files related to 
the handling of Git.

There's two folders on the root directory:

* The [docs](.) folder, which contains all the documentation available for this tool
* The [src](../src) folder which contains the main program ([./src/easy_mqtt_handler/](../src/easy_mqtt_handler)), 
as well as the [scripts/](../src/scripts) folder, which contains shell scripts to assist the build and translation process

Inside the tool's folder ([./src/easy_mqtt_handler/](../src/easy_mqtt_handler)) there's the following structure of subdirectories:

* [assets/](../src/easy_mqtt_handler/assets): contains all icons and graphics needed by the tool
* [licenses/](../src/easy_mqtt_handler/licenses) contains all the license files for all the 3rd party resources used by the tool
* [locale/](../src/easy_mqtt_handler/locale): contains all files needed for the handling of translations
* [qt/](../src/easy_mqtt_handler/qt): contains all the classes created for the QT-GUI. There's a subdirectory for all tabs inside.
* [util/](../src/easy_mqtt_handler/util): contains a selection of common util function