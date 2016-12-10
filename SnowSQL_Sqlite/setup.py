from setuptools import setup

setup(
    name='SnowSQL-Sqlite',
    version='0.1.2',
    description='Python light database framework for sqlite',
    author='Tyan Boot',
    author_email='tyanboot@outlook.com',
    url='https://github.com/tyan-boot/SnowSQL',
    packages=['SnowSQL_Sqlite'],
    keywords='database sql framework',
    install_requires=[
        "SnowSQL >= 0.1.2",
    ]
)
