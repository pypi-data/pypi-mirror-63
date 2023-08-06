import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonschema2rdbmsddl",
    version="0.0.1",
    author="Jacob Joseph",
    author_email="jacob@inciter.io",
    description="Converts JSON Schema to RDBMS DDL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Inciter/jsonschema2rdbmsddl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
