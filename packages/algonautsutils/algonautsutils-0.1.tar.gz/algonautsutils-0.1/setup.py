from setuptools import setup, find_packages

setup(name='algonautsutils',
      version='0.1',
      description='A private repo for maintaining Algonauts utils/tools',
      url='https://bitbucket.org/algonauts/algonautsutils',
      author='Algonauts Technologies',
      author_email='developers@algonauts.in',
      packages=['algonautsutils'],
      install_requires=['numpy',
                        'setuptools',
                        'Flask',
                        'python_dateutil',
                        'kiteconnect==3.7.7',
                        'websocket_client',
                        'psycopg2',
                        'pytz',
                        'scipy'],
      zip_safe=False)
