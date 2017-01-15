from setuptools import setup

setup(
    name='pykhet',
    packages=['pykhet'],  # this must be the same as the name above
    version='0.11',
    description='A general library for the board game khet',
    author='John Mecham',
    author_email='jon.mecham@gmail.com',
    url='https://github.com/TheWiseLion/pykhet',  # use the URL to the github repo
    download_url='https://github.com/TheWiseLion/pykhet/tarball/0.11',
    keywords=['khet', 'boardgame', 'khet2.0', 'laser-chess', 'ai'],  # arbitrary keywords
    classifiers=['Topic :: Games/Entertainment :: Board Games',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5'
                 ],
    install_requires=[
          'enum34',
    ],

)
