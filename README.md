# SPC Native Messaging Host (SPCNMH)

This is required to launch external applications (other browsers, yt-dlp, etc.) from the [Search from Popup or ContextMenu](https://github.com/YoshifumiFuyuno/Search-from-Popup-or-ContextMenu).

See [this page](https://github.com/YoshifumiFuyuno/Search-from-Popup-or-ContextMenu/wiki/Launching-external-apps) for usage.

## Install or Update
Windows:
1. Download [setup.exe](../../releases/latest/download/setup.exe)
1. run exe
1. input 1

Linux, Mac or Windows with Python installed:
1. Download [zip file](../../zipball/master)
1. Extract the zip file to the location where you want to install the software
1. run `python3 ./setup.py` in terminal
1. input 1

For browsers other than Firefox and Microsoft Edge, you may need to rewrite '`allowed_origins: ["chrome-extension://[extensionID]"]`' in the manifest file.  
You can find the extensionID at `chrome://extensions`.

## Uninstall
Windows:
1. run exe
1. input 2
1. remove exe

Linux, Mac or Windows with Python installed:
1. run `python3 ./setup.py` in terminal
1. input 2
1. remove Files
