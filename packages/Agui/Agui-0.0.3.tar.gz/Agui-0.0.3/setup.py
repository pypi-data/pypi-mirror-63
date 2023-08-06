import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Agui",
    version="0.0.3",
    author="Musab Akıcı",
    author_email="musabakici8@gmail.com",
    description="A basic and quick gui application for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akicimusab/Agui",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
