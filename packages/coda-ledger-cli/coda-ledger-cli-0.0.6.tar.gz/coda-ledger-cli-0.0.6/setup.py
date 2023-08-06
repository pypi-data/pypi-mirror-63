import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coda-ledger-cli",
    version="0.0.6",
    author="Rebekah Mercer",
    author_email="rebekah@o1labs.org",
    description="Scripts to interact with the Coda Ledger app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodaProtocol/ledger-coda-app/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "argparse", "base58", "ledgerblue"],
)
