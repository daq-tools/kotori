# -*- coding: utf-8 -*-
# (c) 2023 Andreas Motl <andreas@getkotori.org>
import calendar
import json
from decimal import Decimal
from copy import deepcopy
from datetime import datetime, date

import crate.client.http
import pytz
import requests
from crate import client
from crate.client.exceptions import ProgrammingError
from funcy import project
from twisted.logger import Logger

from kotori.daq.storage.util import format_chunk

log = Logger()


class CrateDBAdapter(object):
    """
    Kotori database backend adapter for CrateDB.

    CrateDB is a distributed and scalable SQL database for storing and analyzing massive
    amounts of data in near real-time, even with complex queries. It is PostgreSQL-compatible,
    and based on Lucene.

    https://github.com/crate/crate
    """

    def __init__(self, settings=None, database=None):
        """
        Carry over connectivity parameters.

        TODO: Verify with CrateDB Cloud.
        """

        settings = deepcopy(settings) or {}
        settings.setdefault("host", "localhost")
        settings.setdefault("port", "4200")
        settings.setdefault("username", "crate")
        settings.setdefault("password", "")
        settings.setdefault("database", database)

        # TODO: Bring back pool size configuration.
        # settings.setdefault('pool_size', 10)

        settings["port"] = int(settings["port"])

        # FIXME: This is bad style. Well, but it is currently
        #        inherited from ~10 year old code, so c'est la vie.
        self.__dict__.update(**settings)

        # Bookkeeping for all databases having been touched already
        self.databases_written_once = set()

        self.host_uri = "{host}:{port}".format(**self.__dict__)

        # TODO: Bring back pool size configuration.
        # log.info('Storage target is {uri}, pool size is {pool_size}', uri=self.host_uri, pool_size=self.pool_size)
        log.info("Storage target is {uri}", uri=self.host_uri)
        self.db_client = client.connect(
            self.host_uri, username=self.username, password=self.password, pool_size=20,
        )

    def get_tablename(self, meta):
        """
        Get table name for SensorWAN channel.
        """
        return f"{meta.database}.{meta.measurement}"

    def create_table(self, tablename):
        """
        Create database table for SensorWAN channel.
        """
        log.info(f"Creating table: {tablename}")
        sql_ddl = f"""
CREATE TABLE IF NOT EXISTS {tablename} (
    time TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    tags OBJECT(DYNAMIC),
    fields OBJECT(DYNAMIC),
    year TIMESTAMP GENERATED ALWAYS AS DATE_TRUNC('year', time)
) PARTITIONED BY (year);
        """.strip()
        cursor = self.db_client.cursor()
        cursor.execute(sql_ddl)
        cursor.close()

    def write(self, meta, data):
        """
        Format ingress data chunk and store it into database table.

        TODO: This dearly needs efficiency improvements. Currently, there is no
              batching, just single records/inserts. That yields bad performance.
        """

        meta_copy = deepcopy(dict(meta))
        data_copy = deepcopy(data)

        try:
            chunk = format_chunk(meta, data)

        except Exception as ex:
            log.failure(
                "Could not format chunk (ex={ex_name}: {ex}): data={data}, meta={meta}",
                ex_name=ex.__class__.__name__,
                ex=ex,
                meta=meta_copy,
                data=data_copy,
            )
            raise

        try:
            success = self.write_chunk(meta, chunk)
            return success

        except requests.exceptions.ConnectionError as ex:
            log.failure(
                "Problem connecting to CrateDB at {uri}: {ex}", uri=self.host_uri, ex=ex
            )
            raise

        except ProgrammingError as ex:
            if "SchemaUnknownException" in ex.message:
                db_table = self.get_tablename(meta)
                self.create_table(db_table)

                # Attempt second write
                success = self.write_chunk(meta, chunk)
                return success

            else:
                raise

    def write_chunk(self, meta, chunk):
        """
        Run the SQL `INSERT` operation.
        """
        db_table = self.get_tablename(meta)
        cursor = self.db_client.cursor()

        # With or without timestamp.
        if "time" in chunk:
            cursor.execute(
                f"INSERT INTO {db_table} (time, tags, fields) VALUES (?, ?, ?)",
                (chunk["time"], chunk["tags"], chunk["fields"]),
            )
        else:
            cursor.execute(
                f"INSERT INTO {db_table} (tags, fields) VALUES (?, ?)",
                (chunk["tags"], chunk["fields"]),
            )
        success = True
        self.databases_written_once.add(meta.database)
        cursor.close()
        if success:
            log.debug("Storage success: {chunk}", chunk=chunk)
        else:
            log.error("Storage failed:  {chunk}", chunk=chunk)
        return success

    @staticmethod
    def get_tags(data):
        """
        Derive tags from topology information.

        TODO: Verify if this is used at all.
        """
        return project(data, ["gateway", "node"])


class TimezoneAwareCrateJsonEncoder(json.JSONEncoder):
    epoch_aware = datetime(1970, 1, 1, tzinfo=pytz.UTC)
    epoch_naive = datetime(1970, 1, 1)

    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime):
            if o.tzinfo:
                delta = o - self.epoch_aware
            else:
                delta = o - self.epoch_naive
            return int(delta.microseconds / 1000.0 +
                       (delta.seconds + delta.days * 24 * 3600) * 1000.0)
        if isinstance(o, date):
            return calendar.timegm(o.timetuple()) * 1000
        return json.JSONEncoder.default(self, o)


# Monkey patch.
# TODO: Submit upstream.
crate.client.http.CrateJsonEncoder = TimezoneAwareCrateJsonEncoder
