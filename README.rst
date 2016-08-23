============
instantshare
============
Takes screenshots and instantly uploads them to an SFTP server, Dropbox, or Google Drive.
As soon as the upload is done, the public URL will be copied to your clipboard.

Providers possibly to be added in the future:

- FTP Servers
- Owncloud (once their API gets updated to Python 3)
- imgur
- ...

At a later point, we would also like to enable you to share other types of media:

- plain text
- any type of file
- audio from a microphone (Opus)
- recorded video (WebM)

Installation
============
At this point, the supported platforms are Microsoft Windows and GNU/Linux.
We might consider adding Mac OSX support at some point in the future.

Currently, we do not ship any binaries or packages, but you can download and extract the sources.
Or just clone the repository to any directory using

.. code-block:: bash
  
    $ git clone https://github.com/instantshare/instantshare.git

Windows
-------
- Download and install Python 3.5: https://www.python.org/downloads/
- Install the dependencies using pip:

    pip install -r requirements.txt

Linux
-----
- Install Python 3.5 using your package manager if it does not come with your distro
- Install ``gnome-screenshot`` and ``xclip`` using your package manager
- Install dependencies using pip (if pip is not installed yet, install python-pip using your package manager)

.. code-block:: bash

    $ pip install -r requirements.txt

Run the app
===========
TODO
