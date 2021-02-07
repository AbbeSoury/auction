from setuptools import setup, find_packages

setup(
    name="auction",
    version="0.1.0",
    packages=find_packages(),
    scripts=[
        "./auction/bin/auction"
    ],
    install_requires=[
        "selenium",
        "click",
        "bs4",
        "pandas",
        "urllib3",
        "flask"
    ],
    author="Melchior P.",
    entry_points='''
        [console_scripts]
        auction=auction.cli.cli:cli
    ''',
    author_email="melchior.prugniaud@gmail.com",
    description="A package to do some auction extraction",
    include_package_data=True
)