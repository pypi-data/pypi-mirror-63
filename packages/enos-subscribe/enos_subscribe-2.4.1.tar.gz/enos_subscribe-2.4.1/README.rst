=======================================
EnOS Data Subscription SDK for Python
=======================================

EnOS Data Subscription Service improves the API calling efficiency of applications with active data push, which supports subscription to real-time asset data, offline asset data, and asset alert data.

After configuring and starting data subscription jobs on the EnOS Management Console, you can use the Data Subscription SDK for Python to develop applications for consuming the subscribed data.

License
=========

 - BSD

Installtion
==============

The Data Subscription SDK for Python supports Python 2.7, Python 3.4, and newer versions.

You can use "python setup.py install" or "pip install enos-subscribe" to install this SDK.

This SDK has the following dependency modules:

 - six
 - google.protobuf
 - websocket_client


Code Sample
==============

Code Sample for Consuming Subscribed Real-time Data
-------------------------------------------------------

.. code:: python

    from enos_subscribe import DataClient

    if __name__ == '__main__':
        client = DataClient(host='sub-host', port='sub-port',
                            access_key='Your Access Key of this subscription',
                            access_secret='Your Access Secret of this subscription')

        client.subscribe(sub_id='Your subscription Id')

        for message in client:
            print(message)


Code Sample for Consuming Subscribed Alert Data
---------------------------------------------------

.. code:: python

    from enos_subscribe import AlertClient

    if __name__ == '__main__':
        client = AlertClient(host='sub-host', port='sub-port',
                            access_key='Your Access Key of this subscription',
                            access_secret='Your Access Secret of this subscription')

        client.subscribe(sub_id='Your subscription Id')

        for message in client:
            print(message)


Code Sample for Consuming Subscribed Offline Data
---------------------------------------------------------

.. code:: python

    from enos_subscribe import OfflineDataClient

    if __name__ == '__main__':
        client = OfflineDataClient(host='sub-host', port='sub-port',
                            access_key='Your Access Key of this subscription',
                            access_secret='Your Access Secret of this subscription')

        client.subscribe(sub_id='Your subscription Id')

        for message in client:
            print(message)
