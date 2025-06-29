==================
pyplotsixel
==================

Matplotlib sixel backend.

It can draw matplotlib figures in SIXEL available terminal.

Install
-----------------

::

   pip install matplotlib
   pip install pyplotsixel


Example
-----------------

Add a `matplotlib.use()` line as follows.

::

   import matplotlib
   import matplotlib.pyplot as plt
   import numpy as np

   matplotlib.use('module://pyplotsixel')


   x = np.linspace(0, 1)
   y = x**2
   plt.plot(x, y)
   plt.show();

Configuration
-----------------

In the `matplotlibrc <https://matplotlib.org/1.4.1/users/customizing.html>`_ ,
if you wrote backend configuration
::

   backend: module://pyplotsixel

you can omit additional `matplotlib.use()` line.
