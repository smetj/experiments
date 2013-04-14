Hammer Grahite
==============

Introduction:
-------------

A sample MetricFactory bootstrap file to dump randomly generated metrics to
one or more Graphite instances.  This could be useful to test Graphite setups
especially when using sharding or some other distributed setup.


Installation:
-------------

- Download and install Metricfactory from https://github.com/smetj/metricfactory
- Download and store the Metricfactory bootstrap file.


Setup:
------

This bootstrap file makes use of following modules:

- metricfactory.test.Hammer: Generates random metrics in the MetricFactory
standard.

- metricfactory.encoder.Graphite: Converts the metrics from
metricfactory.test.Hammer to Graphite format.

- wishbone.module.TippingBucket:  Buffers the metrics coming from
metricfactory.encoder.Graphite until a threshold of X events is reached after
which the buffer is flushed.

- wishbone.iomodule.TCPClient: Writes the data coming from
wishbone.module.TippingBucket to a a list of remote TCP sockets.


Usage:
------

    $ metricfactory debug --config hammer.json

