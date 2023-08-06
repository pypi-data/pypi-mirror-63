import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='zkyhaxpy',  
    version='0.2',
    py_modules=['zkyhaxpy'],
    author="Surasak Choedpasuporn",
    author_email="surasak.cho@gmail.com",
    description="A python package for personal utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/surasakcho/zkyhaxpy",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
 )