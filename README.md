# instantshare
Tool for taking screenshots and instantly sharing them using a number of services.

Currently supported are:
    - Dropbox
    - Google Drive

## Installation
At this point, the supported platforms are Windows and GNU/Linux.
We might consider adding MAC OSX support at some point in the future.

Currently, we do not ship any binaries or packages, but you can download and extract the sources.
Or just clone the repository to any directory using

git clone https://github.com/instantshare/instantshare.git

### Windows
- Download and install Python 3.5: https://www.python.org/downloads/
- Install the dependencies using pip

### Linux
- Install python 3.5 using your package manager
- Install gnome-screenshot using your package manager
- Install dependencies using pip
- You might need to manually change the permissions of the cacerts.txt file used by httplib2 to 644.
  Run "chmod 644 /usr/lib/python3.5/[...]/httplib2/cacerts.txt" as root.