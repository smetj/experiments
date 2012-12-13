ModGearman
==========

Introduction:
-------------

modgearman.json:
Consume Nagios metrics from a ModGearman instance and print them to STDOUT.

modgearman2graphitestdout.json
Consume Nagios metrics from a ModGearman instance, convert them to Graphite format and print them to STDOUT.
If you really want to write the data to Graphite use the wishbone.io_modules.tcpsocketwrite module instead of stdout.

Installation:
--------------
- Download and install Metricfactory from https://github.com/smetj/metricfactory
- Download and store the Metricfactory bootstrap file.

Usage:
------

Print Nagios/Mod_Gearman metrics converted to MetricFactory internal format to STDOUT:
        metricfactory debug --config modgearman.json

Print Nagios/Mod_Gearman metrics converts to Graphite format to STDOUT:
        metricfactory debug --config modgearman2graphitestdout.json


Since Gearmand allows multiple concurrent consumers and Graphite allows concurrent updates you can start multiple instance:
        metricfactory debug --config modgearman2graphitestdout.json --instances 5
