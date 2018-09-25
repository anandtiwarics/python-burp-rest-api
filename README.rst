
Burp REST API
*************

A burp python RESTFul API package.

Requirements
~~~~~~~~~~~~

- `burp-rest-api <https://github.com/vmware/burp-rest-api/>`__
- Burp Suite Professional

Quick Start
~~~~~~~~~~~~

- Install with pip: ``pip install PyBurprestapi``
- Build locally: ``python setup.py build``


Example
~~~~~~~

::


    # import the package
    from burprestapi import burpscanner

    # setup burp connection
    host = 'http://localhost:8090'

    # initialize bi for request
    bi = burpscanner.BurpApi(host)

    # Add target in burp scope
    response = bi.burp_scope('http://testwebsite.com')

    # Get the response message
    print response.message


Bugs and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~

- `If you Found bug or have a feature request? Please open a new issue <https://github.com/anandtiwarics/python-burp-rest-api/issues>`__


