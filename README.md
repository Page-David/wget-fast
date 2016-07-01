# wget-fast
A multithreaded Linux based downloader.
###Features:
wget-fast can dynamiclly start new thread to download.
###Features coming soon:
proxy support, including `.pac` file.

Continue the download if you terminated.

Read URL list file to download.

etc.
## Usage
Download/clone the git repository, unzip it to any where you like, type:

`./wget-fast -s where-to-save-your-file URL`

For example:

`./wget-fast.py -s /home/lancaster/ https://raw.githubusercontent.com/getlantern/lantern-binaries/master/lantern-installer-beta.exe

So far, wget-fast can only download one file in one time, more feature will be updated latter.

## Dependence
`requests`
### Install Dependence
install pip if you have not yet:

`sudo apt-get install python3-pip`

and install package:

`pip3 install requests`
## How to help
It is sweet of you to send pull requests on github.