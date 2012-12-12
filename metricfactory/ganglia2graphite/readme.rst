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

metricfactory debug --config ganglia2graphite.json
