---
modules:
  testevent:
    module: wishbone.builtin.input.testevent
    arguments:
      interval: 0

  header:
    module: wishbone.builtin.function.header
    arguments:
      header:
        mqtt:
          topic: some/topic

  mqtt:
    module: wishbone.output.mqtt
    arguments:
      client_id: wishbone
      host: localhost

routingtable:
  #organize event stream
  - testevent.outbox  -> header.inbox
  - header.outbox     -> mqtt.inbox
...
