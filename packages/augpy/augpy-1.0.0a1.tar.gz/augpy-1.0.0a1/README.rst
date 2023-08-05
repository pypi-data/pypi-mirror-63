augpy
=====

augpy is a lightweight library with minimal dependencies that
provides CUDA tensor functions with a focus on image data
augmentation.
It uses the `dlpack <https://github.com/dmlc/dlpack>`_
standard to export tensors to other libraries, such as
Pytorch, with zero copying.



Building
--------

Make sure you have the following installed.

- Compiler with C++14 support (e.g. GCC 5)
- Cuda 10 or higher
- Cmake 3.13 or higher
- setuptools>=44.0.0
- wheel>=0.34.0
- pybind11>=2.4.3
- numpy>=1.15.0

Now simply run ``setup.py`` as normal to build the wheel and install with pip.

::

    python setup.py bdist_wheel



Usage
-----

TODO



Changelog
---------

1.0.0a1
~~~~~~~

- WIP
