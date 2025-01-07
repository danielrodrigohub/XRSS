# flake8: noqa

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xrss",
    version="0.1.0",
    author="thytu",
    description="Convert Twitter/X feeds to RSS with custom filters and caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thytu/XRSS",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
    ],
    python_requires=">=3.10",
    # Dependencies are now managed in pyproject.toml
    include_package_data=True,
    zip_safe=False,
)
