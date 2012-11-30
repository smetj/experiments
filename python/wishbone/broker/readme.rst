Broker
======

Introduction:
-------------

Dumps a configurable amount of messages in a queue, consumes them and produces
same messages back into that queue which creates a "feedback loop".
The goal of this Wishbone setup is to measure the throughput (msg/s) and to
experiment the performance impact of different AMQP options.

The message rate can be found in the broker management interface.
Use multiple instances for parallel setups.


Usage:
------

./brokertest debug --config brokertest.json --instances 1
