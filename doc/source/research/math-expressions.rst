.. _math-expressions:

################
Math expressions
################

Q: How to evaluate mathematical expressions from a Python string?


Pick
====

Sympy
-----
- http://www.sympy.org/

::

    from sympy import sympify
    sympify('sin(x)').subs({'x': 2}).evalf()


Suitable
========

Simple Eval
-----------
- https://github.com/danthedeckie/simpleeval

Python Mathematical Expression Evaluator
----------------------------------------
- https://github.com/AxiaCore/py-expression-eval
- http://axiacore.com/blog/mathematical-expression-evaluator-python/


All
===

eval
----
- http://lybniz2.sourceforge.net/safeeval.html
- https://opensourcehacker.com/2014/10/29/safe-evaluation-of-math-expressions-in-pure-python/

Pyparsing
---------
- https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string/2371789#2371789
- http://pyparsing.wikispaces.com/file/view/fourFn.py
- http://pyparsing.wikispaces.com/file/view/fourFn.py

AST-based
---------
- https://github.com/danthedeckie/simpleeval
- https://newville.github.io/asteval/
- https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string/9558001#9558001
- https://docs.python.org/2/library/ast.html

Python Parser
-------------
- https://docs.python.org/2/library/parser.html
- https://stackoverflow.com/questions/594266/equation-parsing-in-python/5936822#5936822
- https://stackoverflow.com/questions/594266/equation-parsing-in-python/594294#594294

Python compiler
---------------
- https://stackoverflow.com/questions/594266/equation-parsing-in-python/594360#594360

Misc
----
- https://github.com/pydata/numexpr

.. seealso::

    - https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
    - https://stackoverflow.com/questions/594266/equation-parsing-in-python
    - https://stackoverflow.com/questions/9685946/math-operations-from-string
    - http://www.sagemath.org/

