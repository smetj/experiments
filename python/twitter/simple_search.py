#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  bleh.py
#
#  Copyright 2013 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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

import twitter


def main():
    api = twitter.Api(consumer_key='HrEgYKePpfu3uvUY4vXkA',
        consumer_secret='nGooIgOHBS1jLeCpJUCrnKHRduTng4L8lzXJb8',
        access_token_key='200970553-z754J5z4hMhDrwCG7bqjFyrTv0F5nyRcHfzmGvmX',
        access_token_secret='rfuEcKdc4CzVX7vMq6XnaNqFlGo8KnZtHrFoU7QU4')

    for tweet in api.GetSearch(term="python", count=999):
        print tweet

if __name__ == '__main__':
    main()

