===========
SSH Tunnels
===========

Convenience tool to create SSH tunnels to cluster applications on AWS.

Example cluster applications would be:

* Kafka
* Zookeeper
* Cassandra

This tool automatically adds the private VPC IPs to your local loopback ``lo`` interface
and to your ``/etc/hosts`` file.
Cluster nodes can be accessed directly from your local machine.

.. code-block:: bash

    $ ./tunnels.py my-senza-stack 9092 odd-eu-central-1.myteam.example.org --region eu-central-1
