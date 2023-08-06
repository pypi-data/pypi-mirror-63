from setuptools import setup, find_packages

setup(name='enjoyml',
      version='0.4',
      description='',
      url='https://github.com/ByMyTry/enjoyml.git',
      author='anton-taleckij',
      author_email='anton.taleckij.job@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'pandas',
          'scikit-learn',
          'keras'
      ],
      zip_safe=False)
