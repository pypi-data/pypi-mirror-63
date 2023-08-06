import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_queryset",
    version="0.0.2",
    author="funnyang",
    author_email="2funnyang@gmail.com",
    description="django queryset for script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/funnyang/easy_queryset",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
