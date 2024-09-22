==================
pyplotsixel
==================

Matplotlib sixel backend.

It can draw matplotlib figures in SIXEL available terminal.


Install libsixel
-----------------

In addition to
::

   pip install pyplotsixel

you need to install libsixel  https://github.com/saitoha/libsixel.

I installed libsixel with the Ubuntu apt package as follows.

::

   sudo apt install libsixel-dev


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
   plt.show()

