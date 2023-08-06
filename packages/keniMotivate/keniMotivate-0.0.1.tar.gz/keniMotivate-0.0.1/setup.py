from setuptools import setup

__project__ = "keniMotivate"
__version__ = "0.0.1"
__description__ = "a Python module to motivate you"
__packages__ = ["keniMotivate"]
__author__ = "keni"
__classifiers__ = [
	"Development Status :: 1 - Planning",
	"Environment :: Console",
]
__requires__ = ["guizero"]

setup(
	name = __project__,
	version = __version__,
	description = __description__,
	packages = __packages__,
	author = __author__,
	classifiers = __classifiers__,
	requires = __requires__,
)

