=========================
MasterCard file utilities
=========================

.. image:: https://img.shields.io/travis/adelosa/mciutil.svg
        :target: https://travis-ci.org/adelosa/mciutil

.. image:: https://img.shields.io/pypi/v/mciutil.svg
        :target: https://pypi.python.org/pypi/mciutil

.. image:: https://coveralls.io/repos/adelosa/mciutil/badge.svg?branch=develop&service=github
        :target: https://coveralls.io/github/adelosa/mciutil?branch=develop


Set of command line utilities to work with various MasterCard files.

* Free software: BSD license
* Documentation: https://mciutil.readthedocs.org.

Warning
=======

THIS PACKAGE HAS BEEN DEPRECATED AND WILL NOT BE UPDATED GOING FORWARD

This package was created when I first started learning python. I have learned a lot over the last 4 years
and I now see the error in my ways.

Some of the issues with this module that prompted me to rewrite it:

* memory efficiency - loads entire file into memory for processing. Very ineffient and not very scalable
* programming interface - mciutil did not consider the developer experience. You have to hack to use the logic elsewhere
* dependencies - Too many third party modules, with ones that required a compilation. New version is compile free
* bloat - I used a cookie cutter template when I started and it has stuff I don't like, value or use.
* just mastercard - The old module was for mastercard only but I think it makes sense to have a library for all card utils
* python 2 guff - mciutil works on py2 and 3. There is a lot of gunk in the code to make this work. We live in a py3 world now!

The replacement module is cardutil - see https://cardutil.readthedocs.io
It addresses all of the above issues.


why not just update mciutil?
----------------------------

Thats a good question. I think because the new codebase as developed from scratch rather than
via changes to the existing one (there is some borrowed code from mciutil).
If I just released a new version, anyone leaning on the internal API's would definetly be in trouble
as they are not the same.

Features
========

Provides the following command line utilities:

* paramconv: Utility for working with MasterCard MPE parameter extract files
* mideu: Utility for working with MasterCard IPM files




History
=======

0.6.0 (2018-10-01)
------------------
* Removed dependency on bitarray (no binary wheels)
* Added details on installation for non-python users
* 2 years almost since last update!

0.5.0 (2016-10-03)
------------------
* Fixed version display in release version.
* Removed support for mongo extract

0.4.8 (2016-10-02)
------------------
* added support for latin1 encoding of csv extract
* fixes to setup process so that mideu.yml file is installed
* fixed de43 split to allow more formats for different countries

0.4.6 (2016-08-09)
------------------
* added ``--no1014blocking`` option to allow processing of VBS structure files.

0.4.5 (2016-08-06)
------------------
* check that all of message consumed by fields otherwise raise exception
* get rid of a heap of debugging prints that were clogging the output
* allow freestyle de43 fields with the de43 processor enabled. Use regex rather than string splits

0.4.4-0.4.3 (2016-08-03)
------------------------
* Fix issue with mideu when no parameters passed (stack trace)
* Some more debugging messages provided with -d switch
* signed the release with key for 0.4.4. need to publish my pub key somewhere..

0.4.2 (2016-03-13)
------------------
* Complete data elements added to default config.
* Added versioneer support for easier package versions

0.4.1 (2015-12-16)
------------------
* Additional data elements added to default config file.

0.4.0 (2015-10-05)
------------------
* Now supporting python 2.6 (for all those still using RHEL 6)
* Headers rows in mideu csv extracts don't work in 2.6

0.3.0 (2015-10-03)
------------------
* added sub commands for mideu
* mideu now supports IPM encoding conversion between ascii and ebcdic
* Now faster using list comps instead of slow loops

0.2.0 (2015-08-28)
------------------
* Support for config override for mideu - see usage doco
* Progress bar while using mideu.. it takes a while
* Now supports python 3.4, 3.5 and 2.7. Upgrade if you are using 2.6
* New usage documentation

0.1.0 (2015-08-20)
------------------
* First release.


