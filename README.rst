============
instantshare
============
Tool for taking screenshots and instantly sharing them using a number of services.

Currently supported are:
- Dropbox
- Google Drive

Services to be added in the future:
- FTP, SFTP
- Owncloud
- maybe a specialized self-made Webservice
- ...

Installation
============
At this point, the supported platforms are Windows and GNU/Linux.
We might consider adding MAC OSX support at some point in the future.

Currently, we do not ship any binaries or packages, but you can download and extract the sources.
Or just clone the repository to any directory using

.. code-block:: bash
  
    $ git clone https://github.com/instantshare/instantshare.git

Windows
-------
- Download and install Python 3.5: https://www.python.org/downloads/
- Install the dependencies using pip:

.. code-block:: bash
  
    $ pip install -r requirements.txt

Linux
-----
- Install Python 3.5 using your package manager if it does not come with your distro
- Install gnome-screenshot using your package manager
- Install dependencies using pip
- You might need to manually change the permissions of the cacerts.txt file used by httplib2 to 644.

.. code-block:: bash

    $ sudo chmod 644 /usr/lib/python3.5/[...]/httplib2/cacerts.txt
