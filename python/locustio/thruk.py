#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
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

from locust import Locust, TaskSet, task
from requests.auth import HTTPBasicAuth

class WebsiteTasks(TaskSet):

    @task
    def index(self):
        self.client.get("/thruk", auth=HTTPBasicAuth('guest', 'guest'))

    @task
    def panorama(self):
        headers = {
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
        }
        self.client.get("/thruk/cgi-bin/panorama.cgi", auth=HTTPBasicAuth('guest', 'guest'), headers=headers)

    @task
    def query(self):
        self.client.get("/thruk/cgi-bin/status.cgi?nav=&hidesearch=2&hidetop=&dfl_s0_hoststatustypes=15&dfl_s0_servicestatustypes=31&dfl_s0_hostprops=0&dfl_s0_serviceprops=0&style=detail&update.x=6&update.y=7&dfl_s0_type=servicegroup&dfl_s0_val_pre=&dfl_s0_op=%3D&dfl_s0_value=tag%3Atraffic&dfl_s0_value_sel=5&dfl_s0_type=servicegroup&dfl_s0_val_pre=&dfl_s0_op=%3D&dfl_s0_value=tag%3Adatabase&dfl_s0_value_sel=5&dfl_s0_type=host&dfl_s0_val_pre=&dfl_s0_op=~&dfl_s0_value=workshop&dfl_s0_value_sel=5", auth=HTTPBasicAuth('guest', 'guest'))



class WebsiteUser(Locust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000