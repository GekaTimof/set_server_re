from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
   name='set_server',
   version='1.0',
   description='server for set game. ',
   license='MIT',
   author='Timofeev Evgeniy',
   author_email='geka.timof@mail.ru',
   url='https://github.com/GekaTimof/set_server',
   packages=['server_part'],
   install_requires=requirements,
   extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
   },
   python_requires='>=3',
)