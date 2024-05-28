from setuptools import setup, find_packages

setup(
    name='microservice',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'events @ git+https://github.com/BobryTeam/events.git@pip-deps'
    ],
    author='BobryTeam',
    author_email='sinntexxx@gmail.com',
    description='Base class for all the microservices',
    url='https://github.com/BobryTeam/microservice',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
