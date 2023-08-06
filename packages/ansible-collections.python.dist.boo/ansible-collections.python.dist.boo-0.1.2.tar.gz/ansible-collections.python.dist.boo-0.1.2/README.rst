.. image:: https://img.shields.io/pypi/v/ansible-collections.python.dist.boo.svg?logo=Python&logoColor=white
   :target: https://pypi.org/project/ansible-collections.python.dist.boo
   :alt: ansible-collections.python.dist.boo @ PyPI

.. image:: https://github.com/webknjaz/ansible-collection-python-dist-boo/workflows/Publish%20Python%20🐍%20distributions%20📦%20to%20PyPI%20and%20TestPyPI/badge.svg
   :target: https://github.com/webknjaz/ansible-collection-python-dist-boo/actions?workflow=Publish%20Python%20🐍%20distributions%20📦%20to%20PyPI%20and%20TestPyPI
   :alt: GitHub Actions CI/CD build status — Publish Python 🐍 distributions 📦 to PyPI and TestPyPI

ansible-collections.python.dist.boo: an Ansible Collection containing a boo module
==================================================================================

This is a demo of an `Ansible Collection`_ ``python.dist`` packaged
as a `Python distribution package`_. It contains only one `Ansible
module`_ called ``boo``. Given that this dist and Ansible are
installed into the same (virtual)env, it's accessible from Ansible by
`FQDN`_ ``python.dist.boo``. Here's how you can call it adhoc-style::

    $ PYTHONPATH=`pwd` ansible -m python.dist.boo -a name=Bob localhost
    [WARNING]: No inventory was parsed, only implicit localhost is available
    localhost | SUCCESS => {
        "changed": false,
        "greeting": "Hello, Bob!",
        "msg": "Greeting Bob completed."
    }

Alternatively, install it, instead of mangling with ``PYTHONPATH``::

    $ pip install ansible-collections.python.dist.boo
    $ ansible -m python.dist.boo -a name=Bob localhost
    [WARNING]: No inventory was parsed, only implicit localhost is available
    localhost | SUCCESS => {
        "changed": false,
        "greeting": "Hello, Bob!",
        "msg": "Greeting Bob completed."
    }

.. _`Ansible Collection`:
   https://docs.ansible.com/ansible/devel/dev_guide\
   /developing_collections.html
.. _`Ansible module`:
   https://docs.ansible.com/ansible/devel/dev_guide\
   /developing_program_flow_modules.html
.. _FQDN:
   https://docs.ansible.com/ansible/devel/user_guide\
   /collections_using.html
.. _`Python distribution package`:
   https://packaging.python.org/glossary/#term-distribution-package

Purpose
-------

At the moment of publishing this project, this demo only works with
the code supplied by `Ansible PR #67093`_. One can test it by
installing Ansible from that PR-branch::

    $ pip install git+https://github.com/sivel/ansible@acd-content-dir

.. _`Ansible PR #67093`: https://github.com/ansible/ansible/pull/67093

Publishing to PyPI
------------------

This project implements automatic building and publishing of a Python
distribution package to PyPI for tagged commits and to TestPyPI for
every push to ``master``. All the heavy lifting is done by the
combination of GitHub Actions CI/CD workflows, ``pep517`` CLI tool and
``setuptools-scm``.

The published dists are then installable by::

    $ pip install ansible-collections.python.dist.boo  # for PyPI

and

::

    $ pip install ansible-collections.python.dist.boo \
          -i https://test.pypi.org/simple/ --pre  # for TestPyPI

If you're learning by example, take a look at the following files:

* ``pyproject.toml``
* ``setup.cfg``
* ``.github/workflows/publish-to-test-pypi.yml``

Besides, you can follow a `PyPA guide about publishing packages via
GitHub Actions`_ that will walk you through the process.

.. _`PyPA guide about publishing packages via GitHub Actions`:
   https://packaging.python.org/guides\
   /publishing-package-distribution-releases-\
   using-github-actions-ci-cd-workflows/

Prerequisites
-------------

Python 3.7+

License
-------

The source code and the documentation in this project are released under
the `GPL v3 license`_.

.. _`GPL v3 license`:
   https://github.com/webknjaz/ansible-collection-python-dist-boo\
   /blob/master/LICENSE
