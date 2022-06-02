from setuptools import setup
import jam


setup(
    name="jam",
    version=jam.__version__,
    packages=["jam", "jam.cli"],
    url="",
    license="Apache License 2.0",
    author="max-wi",
    author_email="",
    scripts=["bin/jam"],
    description="Tool to ease development with rez.",
    python_requires=">=3.6.2",
)
