from setuptools import setup

setup(
   name='set_server',
   version='1.0',
   description='server for set game. ',
   license='MIT',
   author='Timofeev Evgeniy',
   author_email='geka.timof@mail.ru',
   url='https://github.com/GekaTimof/set_server',
   packages=['server_part'],
   install_requires=[], # it is empty since we use standard python library
   extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
   },
   python_requires='>=3',
)