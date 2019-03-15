import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haip_database",
    version="0.1.4",
    author="Reinhard Hainz",
    author_email="reinhard.hainz@gmail.com",
    description="A generic database interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haipdev/database",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "asgiref",
        "haip-config",
        "haip-template"
    ]
)
