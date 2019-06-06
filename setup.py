import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scolp",
    version="0.1.4",
    author="David Ohana",
    author_email="davidoha@gmail.com",
    description="Streaming Column Printer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidohana/python-scolp",
    packages=setuptools.find_packages(),
    py_modules=['scolp'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
