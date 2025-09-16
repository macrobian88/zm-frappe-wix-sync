from setuptools import setup, find_packages
import os

# Read requirements
with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# Read README for long description  
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zm_frappe_wix_sync",
    version="0.0.1",
    description="A Frappe app to sync ERPNext items with Wix products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ZM Tech",
    author_email="tech@zmtech.com",
    url="https://github.com/macrobian88/zm-frappe-wix-sync",
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale"
    ],
    project_urls={
        "Bug Reports": "https://github.com/macrobian88/zm-frappe-wix-sync/issues",
        "Source": "https://github.com/macrobian88/zm-frappe-wix-sync",
        "Documentation": "https://github.com/macrobian88/zm-frappe-wix-sync/blob/main/README.md"
    },
)
