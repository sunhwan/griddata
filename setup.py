from setuptools import setup

setup(
    name='griddata',
    version='0.1.0',    
    description='Grid data library for Autodock and OpenDX format files',
    url='https://github.com/sunhwan/griddata',
    author='Sunhwan Jo',
    author_email='sunhwanj@gmail.com',
    license='MIT',
    packages=['griddata'],

    install_requires=[
        'numpy',
    ],

    classifiers=[
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
