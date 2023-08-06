from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'dslgtool',
    version = '0.1.0',
    author = 'longlamduc',
    description = 'A tool to detect image location',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = ['dslgtool'],
    entry_points = {
        'console_scripts': [
            'dslgtool = dslgtool.__main__:main'
        ]
    },
    python_requires='>=3.7',
    )