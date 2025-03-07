.. highlight:: shell

============
Installation
============

Stable release
-------------

YAKE can be installed via pip from GitHub:

.. code-block:: console

    $ pip install git+https://github.com/arianpasquali/yake

This is the preferred method to install YAKE.

Using uv (recommended)
---------------------

YAKE uses `uv <https://github.com/astral-sh/uv>`_ for dependency management.

Install uv:

.. code-block:: console

    $ curl -LsSf https://astral.sh/uv/install.sh | sh

Install the package:

.. code-block:: console

    $ uv sync

Development installation
-----------------------

If you want to install YAKE for development:

.. code-block:: console

    $ uv pip install -e ".[dev]"

From sources
-----------

The sources for YAKE can be downloaded from the `Github repo`_.

You can clone the public repository:

.. code-block:: console

    $ git clone git://github.com/arianpasquali/yake

.. _Github repo: https://github.com/arianpasquali/yake
.. _tarball: https://github.com/arianpasquali/yake/tarball/master
