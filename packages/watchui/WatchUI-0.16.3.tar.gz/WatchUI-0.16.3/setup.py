import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WatchUI", # Replace with your own username
    version="0.16.3",
    author="Jan Egermaier",
    author_email="jan.egermaier@tesena.com",
    description="Compare GUi with RobotFramework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tesena-smart-testing/WatchUI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
