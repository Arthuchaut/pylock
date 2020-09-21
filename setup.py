import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylock",
    version="0.0.1",
    author="Arthuchaut",
    author_email="arthuchaut@gmail.com",
    description="A simple dependencies locker from requirements file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arthuchaut/pylock",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)