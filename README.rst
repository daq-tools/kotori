Setup development sandbox
-------------------------
::

    virtualenv-2.7 --no-site-packages .venv27
    source .venv27/bin/activate

    cd src/ilaundry.node
    python setup.py develop
    cd -

    cd src/ilaundry.master
    python setup.py develop
    cd -


Run daemons
-----------
master::

    ilaundry-master [debug]

go to http://localhost:35000


node::

    ilaundry-node [debug]
