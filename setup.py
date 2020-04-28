from setuptools import setup
setup(name='block_model_cli',
      version='0.1',
      packages=['block_model_cli', 'unit_tests'],
      entry_points={
          'console_scripts': [
              'block_model_cli = block_model_cli.__main__:main',
              'unit_tests = unit_tests.__main__:main'
          ]
      },
      )