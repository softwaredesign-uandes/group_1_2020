from setuptools import setup
setup(name='block_model',
      version='0.1.0',
      packages=['block_model'],
      entry_points={
          'console_scripts': [
              'block_model = block_model.__main__:main'
          ]
      },
      )