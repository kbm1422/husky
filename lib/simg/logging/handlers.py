#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
logger = logging.getLogger(__name__)

import amqp
import json
import socket
import traceback
import urlparse


class AMQPHandler(logging.Handler):
    def __init__(self, url, exchange_name, exchange_type, routing_key):
        logging.Handler.__init__(self)

        result = urlparse.urlparse(url)
        if result.scheme != "amqp":
            raise ValueError

        params = {}
        if result.hostname:
            params["host"] = result.hostname
        if result.username:
            params["userid"] = result.username
        if result.password:
            params["password"] = result.password
        if result.path:
            params["virtual_host"] = result.path

        self.params = params
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key

        self.conn = None
        self.chan = None
        self.__connect()

    def __connect(self):
        self.conn = amqp.Connection(**self.params)
        self.chan = self.conn.channel()
        self.chan.exchange_declare(exchange=self.exchange_name,
                                   type=self.exchange_type,
                                   auto_delete=False,
                                   durable=True)

    def __publish(self, d):
        self.chan.basic_publish(amqp.Message(json.dumps(d), channel=self.chan),
                                exchange=self.exchange_name,
                                routing_key=self.routing_key)

    def emit(self, record):
        d = {k: v for k, v in record.__dict__.items() if k not in ("args", "msg", "exc_info")}
        exc_info = record.__dict__["exc_info"]
        if exc_info is not None:
            d["message"] = d["message"] + "\n" + "".join(traceback.format_exception(*exc_info))

        try:
            self.__publish(d)
        except socket.error:
            #FIXME: add retry when socket error
            # self.conn = None
            # self.chan = None
            # for _ in range(3):
            #     time.sleep(10.0)
            #     self.__connect()
            #     if self.conn and self.chan:
            #         break
            # self.__publish(d)
            pass
        #self.chan.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=json.dumps(d)) #pika

    def close(self):
        self.acquire()
        try:
            #if self.conn and self.conn.is_open: #pika
            if self.conn:
                self.conn.close()
        finally:
            self.release()
        logging.Handler.close(self)

    def __del__(self):
        self.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.NOTSET,
        format='%(asctime)-15s [%(levelname)-8s] - %(filename)s %(lineno)d %(message)s'
    )
