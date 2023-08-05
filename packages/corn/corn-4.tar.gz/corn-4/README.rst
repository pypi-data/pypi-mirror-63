******
CORN
******
**System information discovery and asset tracking**

INSTALLATION
============



Clone the `corn` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/corn.git
    pip install -e corn

EXECUTION
=========
After installation the `corn` command should now be available

Note* Until a vertically app-merged project is also installed
it will have no output

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r corn/requirements-test.txt
    pytest corn/tests

VERTICAL APP-MERGING
====================
Instructions for extending corn for a kernel-specific project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir pop_{kernel}
    cd pop_{kernel}


Use `pop-seed` to generate the structure of a project that extends `corn` and `idem`::

    pop-seed -t v pop_{kernel} -d corn exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d corn exec states" says that we want to implement the dynamic names of "corn", "exec", and "states"

Add "corn" to the requirements.txt::

    echo "corn @ git+https://gitlab.com/saltstack/pop/corn.git" >> requirements.txt

Note* url based reqs aren't supported on older versions of setuptools
To pip install your vertically app-merged project install corn manually::

    pip install -e git+https://gitlab.com/saltstack/pop/corn.git#egg=chunkies

And that's it!  Go to town making corn, execution modules, and state modules specific to your kernel.
Follow the conventions you see in corn.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
