from setuptools import setup, find_packages

setup(
    name="psudo_masker",
    version="0.1.0",
    description="A Python library for pseudonymization using Faker with consistent seeding.",
    author="Midhun Chandrasekhar",
    author_email="csekhar.jr@gmail.com",
    url="https://github.com/kawruhe/psudo_masker.git",
    packages=find_packages(),
    install_requires=[
        "Faker>=18.3.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
