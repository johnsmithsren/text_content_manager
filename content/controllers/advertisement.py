#!/usr/bin/env python
# coding=utf-8
"""Advertisement Controller.

Advertisement controller functions
"""
from __future__ import unicode_literals

import time

from content.models import session_scope
from content.models.entities import News
from content.models.entities import Advertisement
from content.utils import exceptions


def get_advertisement(key):
    with session_scope() as db_session:
        result = db_session.query(Advertisement).filter(Advertisement.key == key).all()
        if result is not None:
            return [results.to_dict() for results in result]
    return None
