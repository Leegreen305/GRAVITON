"""GRAVITON — Exotic Propulsion & Spacetime Engineering Simulator."""

from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(
    encoding="utf-8") if Path("README.md").exists() else ""

setup(
    name="graviton",
    version="0.1.0",
    description="Exotic propulsion and spacetime engineering simulator grounded in peer-reviewed physics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GRAVITON Contributors",
    license="MIT",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.23.0",
        "scipy>=1.9.0",
        "sympy>=1.11",
        "matplotlib>=3.6.0",
        "plotly>=5.11.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": ["pytest>=7.2.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
