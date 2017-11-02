#!/usr/bin/env python
# coding=utf-8
"""News Controller.

News controller functions
"""
from __future__ import unicode_literals

import time

from content.models import session_scope
from content.models.entities import News
from content.models.entities import Advertisement
from content.utils import exceptions


def get_news(key):
    with session_scope() as db_session:
        result = db_session.query(News).filter(News.key == key).first()
        if result is not None:
            return result.to_dict()
    return None


def list_news(page, results_per_page):
    with session_scope() as db_session:
        start = (page - 1) * results_per_page
        end = start + results_per_page
        query = db_session.query(News)
        count = query.count()
        results = query.order_by(News.publish_time.desc()).slice(start, end).all()
        return count, [info.to_dict() for info in results]
    return None