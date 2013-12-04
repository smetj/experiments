Measure total data procuded over the wire
=========================================

A set of Wishbone bootstrap files which generate 100000 metrics in wishbone
Format:


Installation
------------
http://wishbone.readthedocs.org/en/latest/installation.html


Executing
---------

Initializing a Wishbone instance using the provided bootstrap files is done by
executing:

    $ wishbone debug --config wb_mqtt_msgpack.yaml


Data
----

The bootstrap files generate metrics and submit them to the wire using
following protocols:

- Plain TCP
- AMQP
- MQTT

For each protocol metrics are submitted in plain text and in msgpack format.


The generated data looks like:

    (1386189062.3558, 'test', 'hammer', 'hammer.set_99.metric_61', 0, '', ())



Total bandwidth consumed:
-------------------------

+------------+------------+-----------+
|            | plain      | msgpack   |
+============+============+===========+
| TCP        |   12.20 MB |   9.67 MB |
+------------+------------+-----------+
| AMQP       |   26.30 MB |  23.10 MB |
+------------+------------+-----------+
| MQTT       |   10.60 MB |   8.05 MB |
+------------+------------+-----------+
