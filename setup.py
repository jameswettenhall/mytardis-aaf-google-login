import os
from setuptools import setup, find_packages

version = '0.0.1'

setup(name='aaf_google_login',
      version=version,
      description="MyTardis login page for AAF and Google OpenID authentications",
      long_description="""\
MyTardis app to override default login template and use AAF and Google OpenID authentication methods.\
""",
      classifiers=[],
      keywords='MyTardis AAF OpenID',
      author='Manish Kumar',
      author_email='manish.kumar@monash.edu',
      url='',
      license='',
      packages=find_packages(),
      include_package_data=True
      )
