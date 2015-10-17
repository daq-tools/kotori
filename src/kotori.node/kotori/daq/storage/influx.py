# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from influxdb.influxdb08 import InfluxDBClient
from influxdb.influxdb08.client import InfluxDBClientError

class InfluxDBAdapter(object):

    def __init__(self, host='localhost', port=8086, username='root', password='root', database='kotori-dev'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.influx = None

        self.connect()

    def connect(self):
        """
        # production: InfluxDB on localhost
        #database_name = 'kotori_2'
        #self.influx = InfluxDBClient('127.0.0.1', 8086, 'root', 'BCqIJvslOnJ9S4', database_name)

        # development: InfluxDB on Docker host
        database_name = 'kotori-dev'
        self.influx = InfluxDBClient('192.168.59.103', 8086, 'root', 'root', database_name)
        """

        self.influx = InfluxDBClient(
            host=self.host, port=self.port,
            username=self.username, password=self.password,
            database=self.database)

        try:
            self.influx.create_database(self.database)

        except InfluxDBClientError as ex:
            # ignore "409: database kotori-dev exists"
            if ex.code == 409:
                pass
            else:
                raise

    def write(self, name, data):
        columns = data.keys()
        points = data.values()
        data = [
                {
                "name" : name,
                "columns" : columns,
                "points" : [
                    points
                ]
            }
        ]
        self.influx.write_points(data)
        print "Saved event to InfluxDB"
