import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="banditml",
    version="0.0.1",
    author="Edoardo Conti, Lionel Vital",
    author_email="edoardo.conti@gmail.com",
    description="Portable Bandit ML code for training & serving consistency.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/banditml/banditml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pandas", "torch", "sklearn"],
)
