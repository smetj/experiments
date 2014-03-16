
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mqtt.py
#
#  Copyright 2013 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gevent import socket, spawn, sleep
from gevent import event
import struct
import binascii

#MESSAGE TYPE CONSTANTS

CONNECT     = 0b00010000    #  1 Client request to connect to Server
CONNACK     = 0b00100000    #  2 Connect Acknowledgment
PUBLISH     = 0b00110000    #  3 Publish message
PUBACK      = 0b01000000    #  4 Publish Acknowledgment
PUBREC      = 0b01010000    #  5 Publish Received (assured delivery part 1)
PUBREL      = 0b01100000    #  6 Publish Release (assured delivery part 2)
PUBCOMP     = 0b01110000    #  7 Publish Complete (assured delivery part 3)
SUBSCRIBE   = 0b10000000    #  8 Client Subscribe request
SUBACK      = 0b10010000    #  9 Subscribe Acknowledgment
UNSUBSCRIBE = 0b10100000    # 10 Client Unsubscribe request
UNSUBACK    = 0b10110000    # 11 Unsubscribe Acknowledgment
PINGREQ     = 0b11000000    # 12 PING Request
PINGRESP    = 0b11010000    # 13 PING Response
DISCONNECT  = 0b11100000    # 14 Client is Disconnecting


class MQTT():

    def __init__(self, host="127.0.0.1", port=1883, username=False, password=False, client_id="blurp", will_message=False, will_topic=False, will_retain=False, will_qos=False, will_flag=False, clean_session=False, keep_alive=60):
        self.host=host
        self.port=port

        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.client_id=client_id
        self.will_message=will_message
        self.will_topic=will_topic
        self.will_retain=will_retain
        self.will_qos=will_qos
        self.will_flag=will_flag
        self.clean_session=clean_session
        self.keep_alive=keep_alive

        self.expect_next=False

        self.decodePacket = { CONNACK:self._decodeCONNACK}
        self.message_id=1

        self.mtx_publish=event.Event()
        self.mtx_publish.clear()

        self.mtx_read=event.Event()
        self.mtx_read.clear()


        self.__connectSocket(self.host, self.port)
        self.receive=spawn(self.__receiveSocket)

    def connect(self):
        self.__cmdConnect()

    def publish(self, topic, data=False, qos=0, retain=False):
        self.mtx_publish.wait()
        self.__cmdPublish(topic, data, qos, retain)

    def __connectSocket(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))

    def __sendSocket(self, data):
        #print binascii.hexlify(data)
        self._socket.sendall(data)

    def __readSocket(self, bytes=0):
        return self._socket.recv(bytes)

    def __receiveSocket(self):
        while True:
            #Receive 1 byte which should contain the message type
            byte = self.__readSocket(1)
            #if len(byte) > 0:
            byte = struct.unpack("!B", byte)

            if byte[0] == self.expect_next:
                remaining_length=self.__receiveRemainingLengthSocket()
                packet=self.__readSocket(remaining_length+5)
                self.decodePacket[byte[0]](packet)
                self.mtx_publish.set()
            else:
                print "Received output"
                    #unexpected, deal with that

    def __receiveRemainingLengthSocket(self):

        """Expects the next set of bytes to be read from self._socket the
        remaining length bytes.  Returns the number of bytes to read"""

        multiplier = 1
        value = 0
        digit = 128
        while digit & 128 != 0:
            digit = struct.unpack("!B", self.__readSocket(1))[0]
            value += (digit & 127) * multiplier
            multiplier *= 128
        return value

    def _decodeCONNACK(self, packet):

        packet=struct.unpack("!BB", packet)
        if packet[1] == 0:
            return True
        if packet[1] == 1:
            message='Connection Refused: unacceptable protocol version'
        elif packet[1] == 2:
            message='Connection Refused: identifier rejected'
        elif packet[1] == 3:
            message='Connection Refused: server unavailable'
        elif packet[1] == 4:
            message='Connection Refused: bad user name or password'
        elif packet[1] == 5:
            message='Connection Refused: not authorized'
        else:
            message="Return code %s not implemented yet."%(packet[1])
        raise Exception(message)

        self.expect_next=None

    def __cmdConnect(self):
        self.expect_next=CONNACK
        packet = bytearray()

        #Message type
        packet.extend(struct.pack("!B", CONNECT))

        #Variable header
        variable_header=self.__genVariableHeaderConnect()
        packet.extend(variable_header)

        #Payload
        length=0
        for item in [ self.client_id, self.will_topic, self.will_message, self.username, self.password ]:
            if item:
                length+=len(item)
                packet.extend(struct.pack("!H" + str(len(item)) + "s", len(item), item))

        #Remaining length
        print length
        packet[1:1]=self.__calcRemainingLength(len(variable_header) + length + 2)
        self.__sendSocket(packet)

    def __cmdPublish(self, topic, data, qos, retain, dup=False):
        self.expect_next=None
        packet = bytearray()

        remaining_length=0

        #Message type and properties
        command = PUBLISH | ((dup&0x1)<<3) | (qos<<1) | retain
        packet.extend(struct.pack("!B",command))

        #Variable header
        packet.extend(struct.pack("!B",0b00000000))
        remaining_length+=2
        packet.extend(struct.pack("!B",len(topic)))
        remaining_length+=len(topic)

        #Add topic
        packet.extend(struct.pack("!%ss"%(len(topic)),topic))

        #Add message_id if qos defined
        if qos != 0:
            remaining_length+=2
            packet.extend(struct.pack("!B",0b00000000))
            packet.extend(struct.pack("!H",self.message_id))
            self.message_id+=1

        #Add payload
        payload=data.encode('utf-8')
        packet.extend(struct.pack("!%ss"%(len(payload)),payload))
        remaining_length+=len(payload)

        #Add remaining length
        packet[1:1] = self.__calcRemainingLength(remaining_length)

        self.__sendSocket(packet)

    def __genVariableHeaderConnect(self):

        connect_header= int(self.username != False)*128+ \
                        int(self.password != False)*64+ \
                        int(self.will_topic != False)*32+ \
                        int(self.will_retain)*16+ \
                        int(self.will_qos)*8+ \
                        int(self.will_flag)*4+ \
                        int(self.clean_session)*2


        variable_header=bytearray()
        variable_header.append(struct.pack("!B",0b00000000))            # Length MSB (0)
        variable_header.append(struct.pack("!B",0b00000110))            # Length LSB (6)
        variable_header.append(struct.pack("!B",0b01001101))            # M
        variable_header.append(struct.pack("!B",0b01010001))            # Q
        variable_header.append(struct.pack("!B",0b01001001))            # I
        variable_header.append(struct.pack("!B",0b01110011))            # s
        variable_header.append(struct.pack("!B",0b01100100))            # d
        variable_header.append(struct.pack("!B",0b01110000))            # p
        variable_header.append(struct.pack("!B",0b00000011))            # Version (3)
        variable_header.append(struct.pack("!B",connect_header))        # Set connect flags
        variable_header.append(struct.pack("!B",0b00000000))            # Keep alive MSB
        variable_header.append(struct.pack("!B",0b00111100))            # Keep alive LSB (self.keep_alive)
        return variable_header

    def __calcRemainingLength(self, remaining_length):

        result=bytearray()
        while True:
            byte = remaining_length % 128
            remaining_length = remaining_length // 128
            if remaining_length > 0:
                byte = byte | 0x80
            result.extend(struct.pack("!B", byte))
            if remaining_length == 0:
                return result


mqtt=MQTT(host="mosquitto", port=1883, clean_session=True, client_id="mqtt_neekrish_")
mqtt.connect()

#while True:
mqtt.publish(topic="testTopic", data="Test Message", qos=0, retain=False)
mqtt.publish(topic="testTopic", data="Test Message", qos=0, retain=False)
mqtt.publish(topic="testTopic", data="Test Message", qos=0, retain=False)

while True:
    sleep(1)