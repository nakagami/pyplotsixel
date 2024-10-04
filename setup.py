from setuptools import setup

description = "Matplotlib sixel backend"
setup(name="pyplotsixel",
      version="0.2.0",
      description=description,
      long_description=open('README.rst').read(),
      url="https://github.com/nakagami/pyplotsixel",
      author="Hajime Nakagami",
      author_email="nakagami@gmail.com",
      license="BSD",
      keywords=["matplotlib", "sixel"],
      py_modules=["pyplotsixel"])
