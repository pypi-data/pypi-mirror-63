
drf-social-auth  
======================================    
Overview  
--------  
  
Social Authentication For Django Rest Framework  (Google, Facebook, Instagram)
  
Requirements  
------------  
  
-  Python (2.7, 3.3, 3.4)  
-  Django (1.6, 1.7, 1.8)  
-  Django REST Framework (2.4, 3.0, 3.1)  
  
Installation  
------------  
  
Install using ``pip install drf_social``  
 
 
Usage  
-------  
  
1. Add to Installed Apps
`INSTALLED_APPS = [  
  'social_django',  
  'drf_social'  
]`

2. Configure provider at django admin

Customization
-------------

Custom JWT Token Response

1. Inherit from SocialLoginView with custom serializer

Documentation  
-------------  
  
To build the documentation, you’ll need to install ``mkdocs``.  
  
.. code:: bash  
  
    $ pip install mkdocs  
  
To preview the documentation:  
  
.. code:: bash  
  
    $ mkdocs serve  
    Running at: http://127.0.0.1:8000/  
  
To build the documentation:  
  
.. code:: bash  
  
    $ mkdocs build  
  
.. _tox: http://tox.readthedocs.org/en/latest/  
  
.. |build-status-image| image:: https://secure.travis-ci.org/ramzitannous/drf-social-auth.svg?branch=master  
   :target: http://travis-ci.org/ramzitannous/drf-social-auth?branch=master  
.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-social-auth.svg  
   :target: https://pypi.python.org/pypi/drf-social-auth
