from setuptools import setup

setup(
    name = "sgraphic",
    version = "0.1.3",
    author = "Rene Czepluch Thomsen",
    author_email = "sepluk1@gmail.com",
    description = ("Simple graphics. "),
    url="https://github.com/ReneTC/Simple-graphics",
    license = "BSD",
    keywords = "graphics package 2d",
    packages=['sgraphic'],
    install_requires=[
   'skia-python',
   'IPython',
   'Pillow',
   'numpy',
   'easing-functions'

]
)
