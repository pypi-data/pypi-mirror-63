import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TransIp-Restfull-API",  # Replace with your own username
    version="0.1.2",
    author="Mathijs Westerhof",
    author_email="author@example.com",
    description="A python package to connect to the TransIp restfull API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathijswesterhof/TransIp_Rest_api_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)