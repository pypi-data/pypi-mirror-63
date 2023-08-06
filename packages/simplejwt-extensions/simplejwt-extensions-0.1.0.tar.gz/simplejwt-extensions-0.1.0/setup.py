# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplejwt_extensions']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework-simplejwt>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'simplejwt-extensions',
    'version': '0.1.0',
    'description': '',
    'long_description': "Simple JWT Extensions\n=====================\n\nExtensions for the `djangorestframework-simplejwt\n<https://github.com/SimpleJWT/django-rest-framework-simplejwt/>`__ library.\n\nSettings\n--------\n\nAll pre-existing settings for djangorestframework-simplejwt are unchanged. The\nfollowing settings are added and can be set in your ``settings.py`` file:\n\n.. code-block:: python\n\n  # Django project settings.py\n\n  ...\n\n  SIMPLE_JWT = {\n      ...\n      'NEW_USER_CALLBACK': None,\n  }\n\n-------------------------------------------------------------------------------\n\nNEW_USER_CALLBACK\n  A dot path to a callable that is used if the identifier from the token does\n  not match a user in the database. Should return None to fail authentication\n  or a User object to succeed. Will only be used by the\n  JWTTokenAuthenticationSSO backend.\n\nBackends\n--------\n\nJWTTokenAuthentication\n  Use this instead of the ``djangorestframework-simplejwt``\n  ``JWTTokenAuthentication`` backend, to take advantage of features added by\n  this package.\n",
    'author': 'Bequest, Inc.',
    'author_email': 'oss@willing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
