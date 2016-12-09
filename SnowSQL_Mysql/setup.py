from setuptools import setup

setup(
    name='SnowSQL-Mysql',
    version='0.1.1',
    description='Python light database framework for mysql',
    author='Tyan Boot',
    author_email='tyanboot@outlook.com',
    url='https://github.com/tyan-boot/SnowSQL',
    packages=['SnowSQL_Mysql'],
    keywords='database sql framework',
    install_requires=[
        "SnowSQL >= 0.1.1",
        "pymysql"
    ]
)
