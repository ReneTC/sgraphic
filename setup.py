from setuptools import setup

setup(
    name = "sgraphic",
    version = "0.0.5",
    author = "Rene Czepluch Thomsen",
    author_email = "sepluk1@gmail.com",
    description = ("Fast and simple graphics. "),
    url="https://github.com/ReneTC/Simple-graphics",
    license = "BSD",
    keywords = "graphics package 2d",
    packages=['sgraphic'],
    install_requires=[
   'skia-python',
   'IPython',
   'PIL',
   'numpy',
   'easing-functions'

]
)
