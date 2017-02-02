============
instantshare
============
Takes screenshots and instantly uploads them to Imgur, Dropbox, Google Drive, ownCloud or even your own SFTP enabled server.
As soon as the upload is done, the public URL will be copied to your clipboard and you will get a notification to let you know you can start sharing the screenshot with your friends!

Online storage providers possibly to be added in the future:

- FTP Servers
- ... submit your favorite storage provider request via issue or implementation via pull request!

At a later point, we would also like to enable you to share other types of media:

- plain text
- any type of file
- audio from a microphone (Opus)
- recorded video (WebM)

If you find any bugs, please keep in mind that we are still in a very early stage of development.
But if you think that you've got something helpful to add, you are welcome to create a bug report on the `issue tracker`_.

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
- Install ``gnome-screenshot`` and ``xclip`` using your package manager
- Install the dependencies using pip:

.. code-block:: bash

    $ pip install -r requirements.txt

Run the app
===========
If you installed all the dependencies correctly, running the app should be as simple as typing:

::

    > python C:\path\to\instantshare.py

on Windows or

.. code-block:: bash

    $ path/to/instantshare.py

on Linux, replacing the path with the actual location of the file.

Contributing
============
If you want to help, feel free to create a pull request.
Please coordinate your efforts with us first though!

If you don't know much about coding, you can still help. Just visit the `issue tracker`_ and let us know of your ideas!



.. _download: https://github.com/instantshare/instantshare/archive/master.zip
.. _`Python 3.5`: https://www.python.org/downloads/
.. _`issue tracker`: https://github.com/instantshare/instantshare/issues
