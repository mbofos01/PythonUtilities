import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="debugger-decorator",
    version="0.1.0",
    author="Michail Panagiotis Bofos",
    author_email="mbofos@outlook.com",
    description="A comprehensive Python function debugger with colors and caller detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbofos01/PythonUtilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
    ],
    python_requires='>=3.6',
    extras_require={
        'pretty': ['pretty_errors'],
        'colors': ['colorama'],
    },
)
