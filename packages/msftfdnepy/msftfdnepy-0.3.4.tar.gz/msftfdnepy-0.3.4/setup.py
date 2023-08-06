import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msftfdnepy",
    version="0.3.4",
    author="Phil Bennett",
    author_email="phbennet@microsoft.com",
    description="data testing and processing tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://microsoft.com",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyspark'
    ],
    zip_safe=False,
    python_requires='>=3.0'
)