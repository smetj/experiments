UDPSocket
=========

Introduction:
-------------

Demonstrates the usage of the UDP socket input module.


Usage:
------

./udpsockettest debug --config udpsockettest.json

On another terminal:

echo "one2three4"|socat - udp-connect:localhost:10987
