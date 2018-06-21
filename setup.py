from setuptools import setup

setup(name='emailoctopus',
      version='0.1',
      description='Package for EmailOctopus API',
      install_requires=('requests', ),
      url='http://github.com/vivekfantain/emailoctopus.git',
      author='Fantain Sports Private Limited',
      author_email='engineering@fantain.com',
      license='MIT',
      packages=['EmailOctopus', 'EmailOctopus.reports'],
      zip_safe=False)
