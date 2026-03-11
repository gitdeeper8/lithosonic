#!/usr/bin/env python3
# LITHO-SONIC Setup Script

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="lithosonic",
    version="1.0.0",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="Lithospheric Resonance & Infrasonic Geomechanical Observatory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitdeeper8/lithosonic",
    project_urls={
        "Documentation": "https://lithosonic.netlify.app/docs",
        "Source": "https://github.com/gitdeeper8/lithosonic",
        "DOI": "https://doi.org/10.5281/zenodo.18931304",
    },
    packages=find_packages(include=["lithosonic", "lithosonic.*"]),
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "ml": [
            "tensorflow>=2.12.0",
            "torch>=2.0.0",
        ],
        "gpu": [
            "cupy-cuda11x>=12.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lithosonic-init=lithosonic.cli.init:main",
            "lithosonic-collect=lithosonic.cli.collect:main",
            "lithosonic-process=lithosonic.cli.process:main",
            "lithosonic-lsi=lithosonic.cli.lsi:main",
            "lithosonic-serve=lithosonic.cli.serve:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.9, <3.12",
    include_package_data=True,
    zip_safe=False,
)
