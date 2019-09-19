import os 
import sys 
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
  
setup(
  name = 'secure-graphene',         # How you named your package folder (MyLib)
  packages = ['secure_graphene'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python library that assists you in securing your GraphQL API against malicious queries',   # Give a short description about your library
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  author = 'Zachary Manesiotis',                   # Type in your name
  author_email = 'zack.manesiotis@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/manesioz/secure-graphene',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['graphql', 'python', 'security', 'graphene'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'graphql-core',
          'graphene',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
