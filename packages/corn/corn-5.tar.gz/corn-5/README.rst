******
CORN
******
**System information discovery and asset tracking**

INSTALLATION
============
::

    pip install corn

INSTALLATION FOR DEVELOPMENT
============================

Clone the `corn` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/corn.git
    pip install -e corn

EXECUTION
=========
After installation the `corn` command should now be available.

The command will have no output until it is vertically extended (details below).

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r corn/requirements-test.txt
    pytest corn/tests

VERTICAL APP-MERGING
====================
Instructions for extending corn

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir corn_{project_name}
    cd corn_{project_name}


Use `pop-seed` to generate the structure of a project that extends `corn`:

    pop-seed -t v corn_{project_name} -d corn

* "-t v" specifies that this is a vertically app-merged project
*  "-d corn" says that we want to implement the dynamic name of "corn"

Notice that some structure has been created for you.
We especially care about the new directory in `corn_{project_name}/corn`

Add "corn" to the requirements.txt::

    echo "corn" >> requirements.txt

CREATING CORNS
==============
 - Create a new file in "corn_{project_name}/corn"
    - The directory should already have been created by `pop-seed`.
    - The file name is arbitrary.
    - Every file in this directory, then it's subdirectories,  will be parsed "simultaneously" (as far as that makes sense for asyncio).
    - Corns that are dependant on each other should be assigned in the same function.
    - Do NOT rely on the collector's recursion strategy for corns to depend on each other.

 - Add your new project to the python path
    - alternatively, run "pip install -e ." from your project's root directory
        - you only need to do this once

 - Create an async function in this file with a descriptive yet arbitrary name
    - By convention it should start with "load"
    - Make it async unless you have a really really really good reason.
    - Grains that depend on each other already belong in the same function, don't depend on synchronous programming for determinism
    - Corns can be accessed and assigned like a dictionary, but our convention is to use the namespace

Example::

    async def load_my_corn(hub):
        hub.corn.CORN.new_corn = "Hello World!"


And that's it! Now verify that your corn is collected from the command line::

    corn new_corn

Output::

    new_corn:
        Hello World!
