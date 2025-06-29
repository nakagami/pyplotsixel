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

By writing `backend: module://pyplotsixel` in the
`matplotlibrc <https://matplotlib.org/1.4.1/users/customizing.html>`_ ,
you can omit writing, `matplotlib.use('module://pyplotsixel')`.
