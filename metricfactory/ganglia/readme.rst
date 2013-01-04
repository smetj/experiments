Ganglia
=======

Introduction:
-------------

Accept metrics over UDP from a Ganglia client and print the metrics to STDOUT.

Installation:
--------------
- Download and install Metricfactory from https://github.com/smetj/metricfactory
- Download and store the Metricfactory bootstrap file.

Usage:
------

Example 1:
~~~~~~~~~~

Receive Ganglia data over UDP, decode it and print to STDOUT:

	[vagrant@metricfactory-001 ~]$ metricfactory debug --config simple-ganglia-example.json

