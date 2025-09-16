from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in zm_frappe_wix_sync/__init__.py
try:
    from zm_frappe_wix_sync import __version__ as version
except ImportError:
    version = "0.0.1"

setup(
    name="zm_frappe_wix_sync",
    version=version,
    description="A Frappe app to sync ERPNext items with Wix products",
    author="ZM Tech",
    author_email="tech@zmtech.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.8",
    license="MIT",
    keywords=["frappe", "erpnext", "wix", "sync", "ecommerce"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers", 
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    url="https://github.com/macrobian88/zm-frappe-wix-sync",
    project_urls={
        "Bug Reports": "https://github.com/macrobian88/zm-frappe-wix-sync/issues",
        "Source": "https://github.com/macrobian88/zm-frappe-wix-sync",
    },
)
