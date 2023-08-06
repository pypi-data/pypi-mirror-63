import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flixtimeutils",
    version="0.0.1",
    author="SilverCode",
    author_email="hello@silvercode.nl",
    description="Utils for FlixTime python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/FlixTime/utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
