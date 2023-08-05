simple-plotter4a
================

*simple-plotter4a* (i.e. simple-plotter for Android) is an alternative front-end to simple-plotter_ based on kivy_
and the `kivy-garden/graph`_ module.
While it is a cross-platform (completely written in python) its main purpose is to provide a GUI for mobile/touch
devices.

*simple-plotter4a* can be compiled into a stand-alone APK via buildozer_ / `python-for-android`_ and thus requires no
further software installed to run on your Android device.

.. image:: https://simple-plotter.readthedocs.io/en/latest/_images/screen_shot_android.png
    :scale: 25 %

For usage instructions see:
https://simple-plotter.readthedocs.io/en/latest/user_guide.html

*simple-plotter4a* is released under the GPLv3 license - for details see NOTICE and LICENSE file.
The binary version (e.g. Android APK) will be linked and/or bundled with 3rd party libraries. The copyright disclaimers
and licenses of the 3rd party components can be found in the 'Licenses' folder or in the documentation in the licenses
chapter:

https://simple-plotter.readthedocs.io/en/latest/license.html#simple-plotter4a-binary-releases-android

Installing on desktop and Android
---------------------------------

If you just want ot use the software please see the `Getting started`_ chapter in the *simple_plotter* documentation.


Compiling for Android
---------------------

Prerequisites
~~~~~~~~~~~~~

Make sure you have the required components installed - see buildozer_ / `python-for-android`_ documentation for details.

*simple-plotter4a* comes with build instructions for *ant* .
You will need to `Apache ant`_ installed in order to run the build.

Build the APK
~~~~~~~~~~~~~

The *ant* build script (see build.xml) performs some clean-up and version-control tasks before calling the action build
process via *buildozer*.
To build a debug APK simply clone the repository and run *ant* inside:

.. code-block:: bash

    git clone https://gitlab.com/thecker/simple-plotter4a.git
    cd simple-plotter4a
    ant

This will automatically deploy the App to your connected Android device (via adb) and run logcat.

For building (unsigned) release APKs you can run *ant* with the *release* target.

.. code-block:: bash

    ant release


Compiling against a modified version of simple-plotter (base)
-------------------------------------------------------------

By default the base modules of simple-plotter_ will be downloaded and installed via pip from the official PyPI
repository.
If you want to compile the APK against a local, modified base version you should do following.

Make sure, that the modified base is cloned from the git.

.. code-block:: bash

    cd ~/your_work_dir
    git clone https://gitlab.com/thecker/simple-plotter.git

.. note::

    If you use a downloaded zip-file, the compile procedure will fail. Since the *simple-plotter* uses setuptools_scm
    (which is used retrieve the package version from git tags) the package needs to be installed from a valid git
    repository.

Afterwards clone this repo:

.. code-block:: bash

    git clone https://gitlab.com/thecker/simple-plotter4a.git
    cd simple-plotter4a

Edit the *buildozer.spec* and uncomment the *requirements.source.simple-plotter* line and adjust the path
accordingly - e.g.

::

    # (str) Custom source folders for requirements
    # Sets custom source for any requirements with recipes
    requirements.source.simple-plotter = ../simple_plotter

Now start the compilation process with:

.. code-block:: bash

    ant clean-all
    ant

Note to run ``ant clean-all`` to remove any pre-built dependencies (this step, which will make *buildozer* recompile all
dependencies is not required, if you just make changes to *simple-plotter4a*).
It should now compile against your local, modified version of simple-plotter.

.. _simple-plotter: https://gitlab.com/thecker/simple-plotter
.. _kivy: https://kivy.org/#home
.. _kivy-garden/graph: https://github.com/kivy-garden/graph
.. _Apache ant: https://ant.apache.org/
.. _buildozer: https://buildozer.readthedocs.io/en/latest/
.. _`python-for-android`: https://python-for-android.readthedocs.io/en/latest/
.. _`Getting started`: https://simple-plotter.readthedocs.io/en/latest/howto.html
