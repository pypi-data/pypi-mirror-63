from __future__ import print_function

# python
import datetime
import logging
import os
import traceback
from abc import ABCMeta
import queue
import time
import importlib
from flask import current_app as app
from halo_flask.exceptions import StoreException,StoreClearException
from halo_flask.classes import AbsBaseClass
from halo_flask.request import HaloContext
from halo_flask.settingsx import settingsx
from halo_flask.executor import get_executor
from ..exceptions import *

logger = logging.getLogger(__name__)

#https://hackernoon.com/analytics-for-restful-interfaces-579856dea9a9

settings = settingsx()


class BaseEvent(AbsBaseClass):
    __metaclass__ = ABCMeta

    name = None
    time = None
    method = None
    remote_addr = None
    host = None


    dict = {}

    def __init__(self, dict):
        self.dict = dict

    def get(self, key):
        return self.dict[key]

    def put(self, key, value):
        self.dict[key] = value

    def keys(self):
        return self.dict.keys()

    def serialize(self):
        d = {'name':self.name,'time':str(self.time),'method':self.method,'remote_addr':self.remote_addr,'host':self.host}
        if len(self.dict) > 0:
            d.update(self.dict)
        return str(d)


class FilterEvent(BaseEvent):
    pass

class Filter(AbsBaseClass):
    __metaclass__ = ABCMeta

    def do_filter(self,halo_request,  halo_response):
        pass

    def augment_event_with_headers_and_data(self, event, halo_request, halo_response):
        pass

class RequestFilter(Filter):

    def do_filter(self,halo_request,  halo_response):
        logger.debug("do_filter")
        try:
            #catching all requests to api and logging them for analytics
            event = FilterEvent({})
            event.name = halo_request.request.path
            event.time = datetime.datetime.now()
            event.method = halo_request.request.method
            event.remote_addr = halo_request.request.remote_addr
            event.host = halo_request.request.host
            if halo_request.sub_func:
                event.put("sub_func", halo_request.sub_func)
            event = self.augment_event_with_headers_and_data(event, halo_request,halo_response)
            if store_util.clearing():
                inserted = store_util.put(event)
                if (not inserted):
                    logger.debug("Event queue is full! inserted: " + str(inserted) + ", queue size: " + str(StoreUtil.event_queue.qsize()))
                else:
                    logger.debug("Event queue is not clearing! , queue size: " + str(
                        StoreUtil.event_queue.qsize()))
        except StoreException as e:
            logger.debug("error:"+str(e))

    def augment_event_with_headers_and_data(self,event, halo_request,halo_response):
        # context data
        for key in HaloContext.items.keys():
            if HaloContext.items[key] in halo_request.request.headers:
                event.put(HaloContext.items[key],halo_request.request.headers[HaloContext.items[key]])
        return event

class RequestFilterClear(AbsBaseClass):

    def __init__(self, events):
        self.events = events

    def run(self):
        for event in self.events:
            logger.debug("insert_events_to_repository " + str(event.serialize()))

class StoreUtil(AbsBaseClass):
    event_queue = queue.Queue()
    config = None
    flag = False

    def __init__(self, config):
        self.config = config

    def clearing(self):
        if not self.flag:
            executor = get_executor()
            if executor:
                executor.submit(self.start_queue_listener)
                self.flag = True
        return self.flag


    @staticmethod
    def put(event):
        logger.debug("StoreUtil:"+str(event.name))
        try:
            __class__.event_queue.put(event)
            return True
        except Exception as e:
            raise StoreException(e)

    @staticmethod
    def insert_events_to_repository(events):
        logger.debug("insert_events_to_repository")
        # clear to cache/db/other
        if settings.REQUEST_FILTER_CLEAR_CLASS:
            k = settings.REQUEST_FILTER_CLEAR_CLASS.rfind(".")
            module_name = settings.REQUEST_FILTER_CLEAR_CLASS[:k]
            class_name = settings.REQUEST_FILTER_CLEAR_CLASS[k + 1:]
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            if not issubclass(class_, RequestFilterClear):
                raise HaloException("REQUEST FILTER CLEAR CLASS error:" + settings.REQUEST_FILTER_CLEAR_CLASS)
            clazz = class_(events)
        else:
            clazz = RequestFilterClear(events)
        clazz.run()

    @staticmethod
    def start_queue_listener():
        #@todo replace 50 with var default and sleep 5
        logger.debug("start_queue_listener")
        try:
            while (True):
                size = __class__.event_queue.qsize()
                logger.debug("while start_queue_listener "+str(size))
                numberOfIngested = 0;
                if size > 0:
                    events = []
                    maxer = min([50,size])
                    for i in range(0,maxer):
                        event =  __class__.event_queue.get()
                        events.append(event)
                    __class__.insert_events_to_repository(events)
                    numberOfIngested = __class__.event_queue.qsize()
                if numberOfIngested < 50:
                    time.sleep(5);
        except Exception as e:
            logger.debug("Event queue loop broken! , queue size: " + str(
                StoreUtil.event_queue.qsize()))
            raise StoreClearException(e)


store_util = StoreUtil(settings.REQUEST_FILTER_CONFIG)
