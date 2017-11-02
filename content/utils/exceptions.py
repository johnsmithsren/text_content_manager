#!/usr/bin/env python
# coding=utf-8
"""Exceptions

All exceptions
"""
from __future__ import unicode_literals

# error code
# role   x-xx-xxx  level - module - code
# level: 1 - 99
# module: 00: parameters; 01: advertisement; 02: news; 99: http;
# code: 001 002 ...

except_dict = {
    "InsertAdvertisementFailed": {
        "code": "01001",
        "message": "Insert Advertisement Failed.",
        "messageKey": "InsertFailed"
    },
    "DeleteAdvertisementFailed": {
        "code": "01002",
        "message": "Insert Advertisement Failed.",
        "messageKey": "InsertFailed"
    },
    "GetNewsError": {
        "code": "02001",
        "message": "Insert Advertisement Failed.",
        "messageKey": "InsertFailed"
    },
    "AdvertisementNotFound": {
        "code": "01003",
        "message": "Advertisement Not Found.",
        "messageKey": "AdvertisementNotFound"
    },
    "ParamsError": {
        "code": "01004",
        "message": "Params error.",
        "messageKey": "Params error"
    },
    "BadRequest": {
        "code": "01005",
        "message": "Bad request",
        "messageKey": "Bad request"
    },
    "KeyNeed": {
        "code": "01006",
        "message": "Need Key",
        "messageKey": "Need Key"
    },
    "DuplicateKey": {
        "code": "01007",
        "message": "Key already exist",
        "messageKey": "Key already exist"
    }



}


def __init__(self, **kwargs):
    # make returned error message
    self.message = self.message.format(**kwargs)


def __str__(self):
    return self.message


def __repr__(self):
    return self.message


class HttpException(Exception):
    """HTTP Base exception.

    Base exception for all http exception
    """

    pass


exceptions_list = []
bases = (HttpException,)
attrs = {
    '__init__': __init__,
    '__str__': __str__,
    '__repr__': __repr__
}

# generate error classes,
# add them to exception_list
# and then convert to exceptions tuple

for (eklass_name, attr) in except_dict.items():
    attrs.update(attr)
    eklass = type(str(eklass_name), bases, attrs)
    exceptions_list.append(eklass)
    globals().update({eklass_name: eklass})
