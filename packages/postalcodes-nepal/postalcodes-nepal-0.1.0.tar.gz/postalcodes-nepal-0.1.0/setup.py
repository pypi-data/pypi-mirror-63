import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="postalcodes-nepal",
    version="0.1.0",
    author="Biplov",
    author_email="sharmabiplov@gmail.com",
    description="A package for working with postal codes information of Nepal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beingbiplov",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'postalcodes_nepal':['dataset/postalcodes.json']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)