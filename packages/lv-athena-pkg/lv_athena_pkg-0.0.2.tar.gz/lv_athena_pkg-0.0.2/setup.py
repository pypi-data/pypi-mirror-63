import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lv_athena_pkg", # Replace with your own username
    version="0.0.2",
    author="Sofiene Ben Romdhane",
    author_email="sofien@leavy.co",
    description="A package to extract information from s3 via athena",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/leavyco/lv-athena-pck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)