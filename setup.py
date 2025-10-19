# setup.py
from setuptools import setup, find_packages

setup(
    name="workshop",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,  # include non-Python files listed in MANIFEST.in
    install_requires=[
        "beautifulsoup4",
        "pycairo",
        # "PyGObject",
        "markdown",
        "regex"
    ],
    python_requires=">=3.8",
    entry_points={
        # Optional: if you have a CLI script
        "console_scripts": [
            # "workshop.cli = workshop.__main__:main"
        ]
    },
)
