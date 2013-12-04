Measure total data procuded over the wire
=========================================

A set of Wishbone bootstrap files which generate 100000 metrics in wishbone
Format:

Metrics are transport over :

- Plain TCP
- AMQP
- MQTT

For each protocol metrics are submitted in plain text and in msgpack format.


The generated data looks like:
------------------------------

(1386189062.3558, 'test', 'hammer', 'hammer.set_99.metric_61', 0, '', ())


The bootstrap file can executed with:
-------------------------------------

    $ wishbone debug --config wb_mqtt_msgpack.yaml

Installing Wishbone and modules:
--------------------------------
http://wishbone.readthedocs.org/en/latest/installation.html



The total bandwidth consumed:
-----------------------------

tcp_plain               12.20 MB
tcp_msgpack              9.67 MB

amqp_plain              26.30 MB
amqp_msgpack            23.10 MB

mqtt_plain              10.60 MB
mqtt_msgpack             8.05 MB
