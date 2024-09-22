from setuptools import setup

description = "Matplotlib sixel backend"
setup(name="pyplotsixel",
      version="0.1.0",
      description=description,
      long_description=open('README.rst').read(),
      url="https://github.com/nakagami/pyplotsixel",
      author="Hajime Nakagami",
      author_email="nakagami@gmail.com",
      license="MIT",
      keywords=["matplotlib", "sixel", "libsixel"],
      install_requires=["libsixel-python"],
      py_modules=["pyplotsixel"])
