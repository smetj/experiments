Ganglia to Grapĥite
===================

Introduction:
-------------

Accept and buffer metrics from Ganglia clients and write that into Graphite.
Don't forget to use the real address of your Graphite server in the bootstrap file.


Installation:
--------------
- Download and install Metricfactory from https://github.com/smetj/metricfactory
- Download and store the Metricfactory bootstrap file.


Usage:
------

Example 1:
~~~~~~~~~~
If you would like to print the Graphite metrics to stdout then:

	[vagrant@metricfactory-001 ~]$ metricfactory debug --config ganglia2graphite2stdout.json


Example 2:
~~~~~~~~~~
If you would like to submit the metrics directly to Ganglia:

	[vagrant@metricfactory-001 ~]$ metricfactory debug --config ganglia2graphite.json

Example 3:
~~~~~~~~~~
Receive Ganglia data over UDP and balance data to a set of MetricFactory decoders accepting data over Unix domain socket:

        [vagrant@metricfactory-001 ~]$ metricfactory debug --config loadbalance-ganglia.json --pid /tmp/loadbalance-ganglia.pid

Start 5 parallel instances to recieve Ganglia data over Unix Domain socket, decode it and submit to Graphite:

        [vagrant@metricfactory-001 ~]$ metricfactory debug --config uds-ganglia-graphite.json --instances 5 --pid /tmp/uds-ganglia-graphite.pid

