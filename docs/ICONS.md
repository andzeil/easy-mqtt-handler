# Replacing the program icon

The process of changing the program's icon is actually quite simple, but there are some prerequisites. 
First of all, the process was developed and tested on a Linux machine, only. However, in theory it would probably also 
work on a MacOS machine, given you can somehow install the required tooling. Eventually `brew` can help you with this.

First of all make sure that you've got `imagemagick`, `inkscape` and `icnsutils`installed. 
Now open and edit the file `./src/easy_mqtt_handler/assets/app-icon/app-icon.svg`.
Invest all the creativity you can spare and create a new icon. Once done, you should save the file and close your 
image editing tool.

The last step should be actually the easiest one: inside the repos root directory just executed `make regenerate-icons`.
That's it! Afterwards, you should see a lot of different versions of your new icon inside `./src/easy_mqtt_handler/assets/app-icon/`.

If you now build or package the tool again, or even just launch it via Python, you should see your new icon in the tray, already.

If you think you've created a way much nicer icon than I did (and I totally wouldn't blame you!), feel free to contribute it:
just make sure that you've read and understood the guideline on contributing and create a pull request with the content
of your [appicon](../src/easy_mqtt_handler/assets/app-icon/) directory. 