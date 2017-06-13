============
instantshare
============
Instantshare allows you to create media on the fly and upload them to Imgur, Dropbox, Google Drive, ownCloud or even your own server (using SFTP).
As soon as the upload is done, the public URL will be copied to your clipboard and you will get a notification to let you know that you can start sharing your screenshot, paste, voice message or regular file with your friends!

Online storage providers possibly to be added in the future:

- FTP Servers
- Nextcloud
- ... submit your favorite storage provider request via issue or implementation via pull request!

At a later point, we would also like to enable you to share video recorded from your desktop (possibly WebM).

If you find any bugs or if you feel like you've got something helpful to add, you are welcome to contact us on the `issue tracker`_.

Installation
============
At this point, the supported platforms are Microsoft Windows and GNU/Linux.
We might consider adding Mac OSX support at some point in the future.

Currently, we do not ship any binaries or packages, but you can download_ and extract the sources.
Or just clone the repository to any directory using

.. code-block:: bash
  
    $ git clone https://github.com/instantshare/instantshare.git

Windows
-------
- Download and install `Python 3.5`_
- During installation, it is recommended to add Python to your PATH
- Install the dependencies using pip:

::

    > pip install -r requirements-windows.txt

Linux
-----
- Python 3.5 (``python``) and pip (``python-pip``) should come with your distro
- If not, install them using your package manager
- Install using your distro's package manager: ``gnome-screenshot`` ``xclip`` ``python-tk``
- Install the dependencies using pip:

.. code-block:: bash

    $ pip install -r requirements-linux.txt

Run the app
===========
If you installed all the dependencies correctly, running the app should be as simple as typing:

::

    > python C:\path\to\src\instantshare

on Windows or

.. code-block:: bash

    $ path/to/src/instantshare

on Linux, replacing the path with the actual location of the file.

Contributing
============
If you want to help, feel free to create a pull request.
Please coordinate your efforts with us first though!

If you don't know much about coding, you can still help. Just visit the `issue tracker`_ and let us know of your ideas!



.. _download: https://github.com/instantshare/instantshare/archive/master.zip
.. _`Python 3.5`: https://www.python.org/downloads/
.. _`issue tracker`: https://github.com/instantshare/instantshare/issues
