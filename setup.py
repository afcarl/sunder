import sys
from setuptools import setup, find_packages

__version__ = '0.0.1'

if len(set(('test', 'easy_install')).intersection(sys.argv)) > 0:
    import setuptools

extra_setuptools_args = {}
if 'setuptools' in sys.modules:
    extra_setuptools_args = dict(
        test_suite='nose.collector',
        extras_require=dict(
            test='nose>=0.10.1')
    )

setup(
    name="sunder",
    version=__version__,
    description="A small utility for splitting matplotlib Axes.",
    maintainer='Tal Yarkoni',
    maintainer_email='tyarkoni@gmail.com',
    url='http://github.com/tyarkoni/sunder',
    packages=find_packages(),
    license='MIT',
    download_url='https://github.com/tyarkoni/sunder/archive/%s.tar.gz' % __version__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    **extra_setuptools_args
)
