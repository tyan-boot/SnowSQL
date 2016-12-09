from setuptools import setup

setup(
    name='SnowSQL',
    version='0.1.1',
    description='Python light database framework',
    author='Tyan Boot',
    author_email='tyanboot@outlook.com',
    url='https://github.com/tyan-boot/SnowSQL',
    packages=['SnowSQL']
)

setup(
    name='SnowSQL-Sqlite',
    version='0.1.1',
    description='Python light database framework for sqlite',
    author='Tyan Boot',
    author_email='tyanboot@outlook.com',
    url='https://github.com/tyan-boot/SnowSQL',
    packages=['SnowSQL_Sqlite'],
    install_requires = [
        "SnowSQL >= 0.1.1",
    ]
)

setup(
    name='SnowSQL-Mysql',
    version='0.1.1',
    description='Python light database framework for mysql',
    author='Tyan Boot',
    author_email='tyanboot@outlook.com',
    url='https://github.com/tyan-boot/SnowSQL',
    packages=['SnowSQL_Mysql'],
    install_requires = [
        "SnowSQL >= 0.1.1",
        "pymysql"
    ]
)
