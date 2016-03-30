from distutils.core import setup
import setuptools
 
setup(name = "libSpineML",
      version = "0.1",
      description = "Python bindings for the SpineML specifications",
      author = "Adam Tomkins",
      author_email = "a.tomkins@sheffield.ac.uk",
      packages=["libSpineML"],
      install_requires=[
          'lxml >= 3.3.0'
      ]
      )
