#########
Changelog
#########

Release history
===============

1.3.1a1 -- Mon 16 Mar 2020 20:31:24 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fix dependency requirement in ``setup.py`` for ``PyYAML``
* CLI interface now displays help if no option is given

1.3.1a1 -- Mon 16 Mar 2020 03:17:43 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* CLI interface with ``argparser`` and more modularized
* Update documentation

1.2.1a1 -- Sun 15 Mar 2020 17:16:17 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Improve code readability to comply with :PEP:`8` and :PEP:`257`
* Divide code into one more file, for file operations
* Generate pages slug from the title, like posts, not the filename
* Error codes
* Reduce redundant code in ``Builder`` class, private methods to manage
  the code better
* Refactorize the code

1.2.0a1 -- Sun 15 Mar 2020 10:44:17 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Logging support by using ``logging``.  Warnings and errors stored in
  separated file, information logs (or more critical) on ``stdout``.
  When the CLI interface will be updated with ``argparser``, the user
  will be able to select the log level, DEBUG (show all), INFO (show
  only file updates, but not parsing actions), WARNING,...

1.1.0a1 -- Sat 14 Mar 2020 01:21:35 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Pages now are stored in the directory ``pages``
* Generate links to pages in the navigation bar, unless indicating the
  opposite.
* Fix bugs.

1.0.2.dev4 -- Wed 12 Mar 2020 02:24:35 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fix tarball in PIP repository

1.0.0.dev1 -- Wed 11 Mar 2020 03:21:35 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* First tests finished, released as 1.0.0-alpha and first steps into
  package developing
* Move all templates to user space, so the user has full
  control over the presentation, and prepares the system for future
  inclusion of themes
* Rebrand as **PynFact!** (without the apostrophe)

0.4.0 -- Tue 10 Mar 2020 16:44:33 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Esperanto locale added (``eo``) using ``gettext``
* Esperanto meta tags available
* Remove deprecated ``safe_mode`` in Markdown calls
* Fixed some bugs

0.3.8 -- Mon 09 Mar 2020 15:34:52 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Simplify ``Builder`` class constructor: now it takes a configuration
  dicionary sorted semantically
* Refactorize and improved exceptions check

0.3.7 -- Mon 09 Mar 2020 11:46:19 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Remove Javascript and added light/dark CSS styles
  
0.3.6 -- Wed 04 Mar 2020 15:30:48 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Enable/disable comments by option in configuration file

0.3.5 -- Tue 03 Mar 2020 15:36:29 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Minor bugs and refactoring

0.3.4 -- Tue 03 Mar 2020 14:27:04 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Files that haven't changed are no longer rewritten after parsing the
  Markdown text; only overwritte those files that are different (using
  ``filecmp``)

0.3.3 -- Tue 03 Mar 2020 08:23:24 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Convert into git repository instead of mercurial [#]_

0.3.2 -- Mon 02 Mar 2020 15:39:12 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Update existing parsed files only if they are different (*diff*)

0.3.1 -- Sun 01 Mar 2020 16:02:01 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Restore categories support

0.3.0 -- Sat 29 Feb 2020 14:27:36 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Replace ``feedgen`` for ``pyatom`` to generate RSS/Atom syndication
  feeds
* Remove categories (temporarily) for testing purposes

0.2.3 -- Wed 24 May 2017 19:36:50 +0200
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Update default first entry (extension reference)
* Change posts default extension, from ``.mdown`` to ``.md``

0.2.2 -- Mon 22 May 2017 10:27:35 +0200
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Minimal update of CSS and templates

0.2.1 -- Sun 18 Dec 2016 21:28:59 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Update ``README.md`` file
* Fix dates since old commit (in another repository)

0.2.0 -- Sun 11 Dec 2016 15:42:25 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add support for categories
* Release as v. 0.2.0 and repository regenerated

0.1.3 -- Thu 22 Oct 2015 16:14:15 +0200
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Review: routine control, ``cli.py``, and author updated

0.1.2 -- Sat 22 Feb 2014 15:52:46 +0100
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Review: routine control
* Add locale support, including:
  * English
  * Spanish
  * Portuguese
  * Galician
  * Catalan

0.1.1 -- Sun 02 Jun 2013 16:23:48 +0200
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fix bugs and correct code

0.1.0 -- Mon 22 Oct 2012 16:29:06 +0200
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* *Py'nFact!* initial developing version using Python 3.6 (0.1.0)
* Default listen address: ``http://127.0.0.1:4000``


.. [#] There was no importation, no preservation of logs, or anything
       similar.  This is a personal project being developed just buy one
       person, so there was no need to import the entire Hg repository
       logs.

