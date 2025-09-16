from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in zm_frappe_wix_sync/__init__.py
from zm_frappe_wix_sync import __version__ as version

setup(
    name="zm_frappe_wix_sync",
    version=version,
    description="A Frappe app to sync ERPNext items with Wix products",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
