UDPServer
=========

Introduction:
-------------

Demonstrates the usage of the UDP socket input module.


Usage:
------

	./udpserver debug --config udpserver.json

On another terminal:

	echo "one2three4"|socat - udp-connect:localhost:10987
