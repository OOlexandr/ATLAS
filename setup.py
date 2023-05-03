from setuptools import setup, find_namespace_packages

setup(
    name='ATLAS',
    version='1',
    description='ArTificial command Line ASsistant',
    url='https://github.com/OOlexandr/ATLAS',
    author_email='oleksarkhumua@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={
   'console_scripts': [
       'atlas = Atlas\ATLAS.atlas:main',
       ]
   },
   install_requires=['prompt_toolkit'],
   include_package_data=True
)