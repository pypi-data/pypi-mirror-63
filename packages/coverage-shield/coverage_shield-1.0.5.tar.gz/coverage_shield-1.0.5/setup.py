from distutils.core import setup

with open('README.md') as f:
    README = f.read()

setup(
    name='coverage_shield',
    packages=['coverage_shield'],
    version='1.0.5',
    description='Uploads total coverage for displaying badge',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=['coverage'],
    author='Samuel Carlsson',
    author_email='samuel.carlsson@volumental.com',
    url='https://github.com/Volumental/badges',
    keywords=['coverage', 'badge', 'shields.io'],
)
