import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nod-labs-NNS", # Replace with your own username
    version="0.0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    author="Nod Labs",
    author_email="bingyu@nod-labs.com",
    description="Nod AutoML package for neural architecture search and model training of image classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nod.com",
#    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    
)
