=============
Parallel TQDM
=============


.. image:: https://img.shields.io/pypi/v/pqdm.svg
        :target: https://pypi.python.org/pypi/pqdm

.. image:: https://img.shields.io/travis/niedakh/pqdm.svg
        :target: https://travis-ci.com/niedakh/pqdm

.. image:: https://readthedocs.org/projects/pqdm/badge/?version=latest
        :target: https://pqdm.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/niedakh/pqdm/shield.svg
     :target: https://pyup.io/repos/github/niedakh/pqdm/
     :alt: Updates



PQDM is a TQDM and concurrent futures wrapper to allow enjoyable paralellization of progress bars.


* Free software: MIT license
* Documentation: https://pqdm.readthedocs.io.


Install & Use
-------------

To install ::

    pip install pqdm


and use ::

    from pqdm.processes import pqdm
    # If you want threads instead:
    # from pqdm.threads import pqdm

    args_1 = [1, 2, 3]
    args_2 = [2, 3, 4]

    def multiply(a,b):
        return a*b

    pqdm(zip(args_1, args_2), argument_type='args', n_jobs=2)


Features
--------

* parellize your tqdm runs using processes or threads thanks to concurrent.futures,
* just import ``pqdm`` from ```pqdm.threads``` or ```pqdm.processes``` to start,
* automatic usage of ```tqdm.notebook``` when iPython/Jupyter notebook environment detected,
* automatic parsing of ```pqdm``` kwargs and separating between ```concurrent.Executor``` args and ```tqdm``` args,
* support for any iterable and passing items as kwargs, args or directly to function which is being applied
* support bounded exectutors via https://github.com/mowshon/bounded_pool_executor

Credits
-------

Written by Piotr Szymański <niedakh@gmail.com>.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
