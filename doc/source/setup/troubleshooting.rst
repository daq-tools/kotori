###################################
Troubleshooting installation issues
###################################

Sometimes, things go south.


When installing the development sandbox by typing::

    make virtualenv-dev

Building wheels for collected packages: pycrypto::

    src/_fastmath.c:36:11: fatal error: 'gmp.h' file not found
    # include <gmp.h>
              ^~~~~~~
    197 warnings and 1 error generated.

Solution::

    export CPPFLAGS=-I/usr/local/opt/gmp/include
    export LDFLAGS=-L/usr/local/opt/gmp/lib
    make virtualenv-dev
