UDSServer
=========

Introduction:
-------------

Demonstrates the usage of the Unix Domain Socket input module.

Usage:
------

./udsserver debug --config udsserver.json

On another terminal:

echo "one2three4"|socat - UNIX-CONNECT:/tmp/udsserver
