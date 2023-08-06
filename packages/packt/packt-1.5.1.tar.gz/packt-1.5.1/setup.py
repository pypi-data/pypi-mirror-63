import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

package_version = '1.5.1'

requirements = [
    'click==7.0',
    'google-api-python-client==1.6.3',
    'requests==2.20.0',
    'python-slugify==4.0.0'
]

dev_requirements = [
    'bumpversion==0.5.3',
    'mccabe==0.6.1',
    'pycodestyle==2.5.0',
    'pyflakes==2.1.1',
    'pylama==7.7.1',
    'twine==1.15.0'
]

setup(
    name='packt',
    version=package_version,
    license='MIT',
    description='Script for grabbing daily Packt Free Learning ebooks',
    author='Łukasz Uszko',
    author_email='lukasz.uszko@gmail.com',
    url='https://github.com/luk6xff/Packt-Publishing-Free-Learning',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    py_modules=['packtPublishingFreeEbook', 'api', 'claimer', 'configuration', 'downloader'],
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    entry_points={
        'console_scripts': [
            'packt-cli = packtPublishingFreeEbook:packt_cli',
        ],
    },
    download_url='https://github.com/luk6xff/Packt-Publishing-Free-Learning/archive/v1.5.1.tar.gz',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
