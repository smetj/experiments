DomainSocket
============

Introduction:
-------------

Demonstrates the usage of the domain socket input module.
In this example the server is running in blob mode.

Usage:
------

./domainsockettest debug --config domainsockettest.json

On another terminal:

echo "one2three4"|socat - UNIX-CONNECT:/tmp/domainsocket
