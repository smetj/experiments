TCPServer
=========

Introduction:
-------------

Demonstrates the usage of the TCP socket input module.

Usage:
------

	$ wishbone debug --config udsserver.json

On another terminal:

	$ echo "one2three4"|socat - tcp4-connect:localhost:10999
