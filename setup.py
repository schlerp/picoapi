import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="picoapi",
    version="0.1.5",
    author="Patrick Coffey",
    author_email="patrickcoffey91@gmail.com",
    description="An opinionated wrapper around FastAPI with custom microservice registration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schlerp/picoapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pydantic",
        "fastapi",
        "requests",
    ],
    python_requires=">=3.6",
)
