Licenses of dependencies
========================

This folder contains the License files of the 3rd party components used to build the Android APK for
*simple-plotter4a* and a table *p4a_dependencies* (*.ods and *.csv version) which summarizes the dependencies.

The *create_attributions.py* script will extract the information from the *p4a_dependencies.csv* file and generate a
couple of files:

../simple_plotter4a/data/attributions_android_<release_version>.txt
    This text file contains a formatted version of the attributions - package/library name, version (if existing),
    Copyright (if existing) and source (e.g. URL) - of the individual 3rd party components. This text will be displayed
    as a scrolling text in the Android app's license screen.

../simple_plotter4a/data/attributions_python_<release_version>.txt
    This text file contains a formatted version of the attributions - package/library name and source (e.g. URL) - of
    the individual 3rd party python dependencies. This text will be displayed  as a scrolling text in the desktops
    app's license screen.

./attributions_<release_version>.rst
    An ReStructuredText file including the attributions and the full license text of the individual 3rd party
    components. This file is copied into the *simple-plotter* documentation and shall be referenced in the Android app's
    license screen.

.. note::

    The versions of the 3rd party components must be adjusted to match the versions of the recipes of the used
    *python-for-android* distribution and the PyPI package versions, when a release *simple-plotter4a* is build.