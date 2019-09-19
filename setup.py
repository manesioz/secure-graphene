import os 
import sys 
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
  
setup(
  name = 'secure-graphene',         
  packages = ['secure_graphene'],  
  version = '0.1',      
  license='MIT',        
  description = 'Python library that assists you in securing your GraphQL API against malicious queries',   
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  author = 'Zachary Manesiotis',        
  author_email = 'zack.manesiotis@gmail.com',    
  url = 'https://github.com/manesioz/secure-graphene',   
  download_url = 'https://github.com/manesioz/secure-graphene/archive/v1.0.tar.gz',    
  keywords = ['graphql', 'python', 'security', 'graphene', 'api'],   
  install_requires=[
          'graphql-core',
          'graphene',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
