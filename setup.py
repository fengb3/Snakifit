from setuptools import setup, find_packages

setup(
    name="http-client-py",
    version="0.1.0",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="fengb3",
    author_email="your.email@example.com",
    url="https://github.com/fengb3/http-client-py",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        "requests",
        "urllib3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
