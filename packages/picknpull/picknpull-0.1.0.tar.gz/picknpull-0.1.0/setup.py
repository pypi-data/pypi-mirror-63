import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="picknpull",
    version="0.1.0",
    author="James Scheiber",
    author_email="jscheiber22@gmail.com",
    description="An automated search for the Pick N Pull website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/jscheiber22/pick-n-pull-automated-search/src/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
