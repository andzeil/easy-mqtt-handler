# Packaging Easy MQTT Handler

## Packaging on Linux

### Dependencies
Usually, the only dependency you will need for packaging on Linux is Python 3(.11). While there are a lot more dependencies
you shouldn't have to worry about them, as the build system we're using (briefcase) should set them all up for you.
All the provided steps have been tested on Ubuntu 23.04 (64bit). They may or may not work with other Linux distributions and versions. 
Please open a pull request to the documentation should you discover there are more steps needed for 
other Linux flavors. Just install Python3 with the package manager of your choice, and you should be ready to go.

In case you are having problems with the briefcase build system, you can still try to install dependencies in an 
automated fashion via `make activate-venv`. If even this is no option (maybe because of the very unlikely reason that 
your system doesn't even offer `make`), you can also try to install them via `pip install -r requirements.txt`.
All the listed commands should be executed inside the repos root directory.

### Packaging process

In the shell of your choice navigate to the folder of Easy MQTT Handler's source code and execute the following command:
`make package`

To build a package which should suite the Linux Distribution you are running on to build the package. You should find
your package in the **dist** subdirectory, afterwards.

***

## Packaging on Windows

### Dependencies
Usually, the only dependency you will need for packaging on Windows is Python 3(.11). While there are a lot more dependencies
you shouldn't have to worry about them, as the build system we're using (briefcase) should set them all up for you.
All the provided steps have been tested on Windows 10 (64bit). They may or may not work with other Windows versions. 
Please open a pull request to the documentation should you discover there are more steps needed for 
other Windows versions. You should download and install the latest Python 3(.11) installer from: 
https://www.python.org/downloads/ (select the amd64 installer)

### Packaging process

Via **cmd.exe** or **powershell.exe**, in the folder of Easy MQTT Handler's source code, execute the following commands:

		C:\[..]> py -m venv .venv
		C:\[..]> .venv\Scripts\activate.bat
		(.venv) C:\[..]> briefcase package

Once **briefcase** finished packaging you can find the installer's **.msi** file in the **dist** subdirectory

***

## Packaging on MacOS

### Dependencies

**!!! Please be aware that the content of this documented is untested, as I don't own an  Apple Machine. 
I can unfortunately not support you if you are facing any issues. Please open a pull request to the documentation should
you discover any error in these instructions !!!**

On MacOS you should first install `brew` a free package manager that helps you to install a lot of different Unix tools.
You can all you need to get started on the [brew website](https://brew.sh/#install). Once you have `brew` installed
execute the following command on your shell: `brew install python@3.11`

For convenience reasons you should probably also install `make` via brew, by executing: `brew install make`.

This should usually be it!

### Packaging Process

Now you should be able to build a package via `make build-macos-app`.

In case you are having problems with the briefcase build system, you can still try to install dependencies in an 
automated fashion via `make activate-venv`. If even this is no option (maybe because you are having 
problems installing `make`), you can also try to install them via `pip install -r requirements.txt`. 
All the listed commands should be executed inside the repos root directory.

Once **briefcase** finished packaging you can package in the **dist** subdirectory

Even if you aren't able to build the tool for whatever reason, you might now be able to at least use it via
`python3 ./__main__.py` (run this inside src/easy_mqtt_handler!)

***

## Replacing the program icon

If you want to change the icon of the program, which I can totally understand, as I'm absolutely no artist and this is 
actually the first icon I've ever really created and published, you can do so easily. Just checkout the documentation
provided here: [ICONS.md](ICONS.md)