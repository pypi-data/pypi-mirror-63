import os

from setuptools import find_packages, setup

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"),
    encoding="utf-8",
) as f:
    long_description = f.read()

setup(
    name="proust",
    version="0.1.2",
    author="Daniel Suo",
    author_email="danielsuo@gmail.com",
    description="Online time series analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielsuo/proust",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["timeseries", "time", "series", "analysis"],
    python_requires=">=3.5",
    install_requires=[
        "numpy",
        "scipy",
        "cython",
        "jax",
        "jaxlib",
        "scikit-learn",
        "matplotlib",
    ],
    extras_require={
        "dev": [
            "flake8",
            "flake8-print",
            "flake8-bugbear",
            "mypy",
            "pytest",
            "pytest-xdist",
            "pytest-cov",
            "pylint",
            "black",
            "isort",
            "autoflake",
            "pre-commit",
            "pydocstring-coverage",
            "bumpversion",
        ]
    },
)
