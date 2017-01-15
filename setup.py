from distutils.core import setup

setup(
    name='pykhet',
    packages=['pykhet'],  # this must be the same as the name above
    version='0.1',
    description='A',
    author='John Mecham',
    author_email='jon.mecham@gmail.com',
    url='https://github.com/TheWiseLion/pykhet',  # use the URL to the github repo
    download_url='https://github.com/TheWiseLion/pykhet/tarball/0.1',
    keywords=['khet', 'boardgame', 'khet2.0', 'laser-chess', 'ai'],  # arbitrary keywords
    classifiers=[],
    install_requires=[
          'enum34',
    ]
)
