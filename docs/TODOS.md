# TODOs / known issues

* Implement Tests -> there are absolutely no tests implemented right now.
* Add some batch scripts to assist Windows users in building and packaging.
* Improve exception handling. I kid you not: it's actually quite poor, honestly.
* Add GitHub Actions build pipeline to automatically publish binaries for users to download.
* Look into adding some dependency scanner. The project doesn't use many, but I guess that's no excuse.
* Improve communication between the WorkerThread and the Main Window. The current implementation uses hardcoded IDs and mappings, rather bad.
* Implement more options for the tool. Stuff like "show main window on start", "display tray icon", etc. should be configurable.
* Implement a GUI-less option, maybe an accompanying daemon / service.
* Fix the way commands are executed. Right now MQTTWorkerThread just uses the os.system() call, which is problematic because of how process usually work.
* Fix the way QTableView is implemented: it's actually quite hacky and shady right now ... but hey: at least it gets the job done!
* Implement more command line arguments.
* Maybe allow more than one connection and one list of payload handlers.
* Figure out why the packaging process seems to hang on MacOS (at least on [@guitmz's](https://github.com/guitmz/) machine -> thanks for your support btw, mate!)
* Maybe publish the tool on the Windows and / or Apple Store to make it convenient for users to install it on their machines.
* You tell me -> [GitHub issues](https://github.com/andzeil/easy-mqtt-handler/issues)! 😄
