import os
from setuptools import setup


def readme(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='audioTranscription',
    version='1',
    packages=['audioTranscription'],
    url='',
    license='',
    author='marcus.freitas',
    author_email='marcus.freitas@gmx.net',
    description='Python script to convert audio files to text',
    long_description=readme('README'),
    install_requires=[
        'SpeechRecognition',
        'pydub',
    ]
)
