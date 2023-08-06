import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stimekeeper", # Replace with your own username
    version="0.0.1",
    author="Strat 365",
    author_email="Ron@Diasly.com",
    description="Times Up Philosophy. Think of yourself as dead",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/strat365/timekeeper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)