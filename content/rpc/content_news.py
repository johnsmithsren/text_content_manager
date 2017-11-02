#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

import json
from content.utils import exceptions
from content.models import session_scope
from content.models.entities import News
from content.models.entities import Advertisement
import time
import re
from flask import session
from flask import request
from flask import jsonify
from content.utils import genenrate_news as news_controller
from content.utils import templates
from flask import Blueprint
from content.rpc import rest as restless_query
from sqlalchemy import text
from pypinyin import pinyin, lazy_pinyin, Style

symbol = {"eq": "=", "neq": "!=", "gt": ">",
          "ge": ">=", "lt": "<", "like": "like"}


def get_news(id):
    with session_scope() as db_session:
        result = db_session.query(News).filter(News.id == id).first()
        if result is not None:
            return result.to_dict()
        return None
    return None


def get_news_by_key(key):
    with session_scope() as db_session:
        result = db_session.query(News).filter(News.key == key).first()
        if result is not None:
            return result.to_dict()
        return None
    return None


def list_news(page, results_per_page, type=None):
    with session_scope() as db_session:
        support_columns = ("key", "title", "content",
                           "source_from", "source_url", "status")
        start = (page - 1) * results_per_page
        end = start + results_per_page
        query = db_session.query(News)
        _filter = None
        if type is not None:
            for _info in type:
                for item in support_columns:
                    if item in _info:
                        _symbol = _info.get("op", 'op')
                        _type = _info[item]
                        if symbol.get(_symbol, "=") == "like":
                            _type = "%" + ("%s" % (_info[item])) + "%"
                        _filter = "`%s` %s '%s' " % (
                            item, symbol.get(_symbol, "="), _type)
                if _filter is not None:
                    query = query.filter(text(_filter))
        count = query.count()
        results = query.order_by(
            News.create_time.desc()).slice(start, end).all()
        data = [info.to_dict(exclude_columns=["content"]) for info in results]
        total_pages = count / \
            results_per_page if count % results_per_page == 0 else count / results_per_page + 1
        return {
            "code": 0,
            "data": {
                "objects": data,
                "total_pages": total_pages,
                "current_page": page,
                "num_results": count
            }
        }
    return None


def update_news(id, data):
    with session_scope() as db_session:
        result = db_session.query(News).filter(News.id == id).first()
        now = int(time.time())
        if result is None:
            return None
        support_columns = ("key", "title", "summary", "content", "source_from",
                           "icon", "source_url", "publish_time", "to_static", "status")
        for column in support_columns:
            if column in data:
                setattr(result, column, data[column])
        _data = data.get("status", None)
        if int(_data) == 1:
            result.publish_time = now
            result.to_static = 1
        else:
            result.publish_time = None
            result.to_static = 1
        db_session.add(result)
        db_session.commit()
        news_controller.news_template.delay()
        return result.to_dict()
    return None


def delete_news(id):
    with session_scope() as db_session:
        db_session.query(News).filter(News.id == id).delete(False)
        db_session.commit()
        news_controller.news_template.delay()
        return True
    return None


def create_news(data):
    with session_scope() as db_session:
        title = data.get("title", None)
        if title is None:
            raise exceptions.ParamsError()

        title = re.sub(u'[^a-zA-Z0-9\-\u4e00-\u9fa5]',
                       '', title.decode('utf-8'))

        key = lazy_pinyin(title)
        _key = '-'.join(key[0:5])

        now = int(time.time())
        new = News()
        new.set_create_table_base()
        support_columns = ("title", "content", "source_from",
                           "summary", "icon", "source_url", "publish_time", "status")
        for column in support_columns:
            if column in data:
                setattr(new, column, data[column])
        new.to_static = 0
        _data = data.get("status", None)
        if int(_data) == 1:
            new.publish_time = now
            new.to_static = 1
        else:
            new.publish_time = None
            new.to_static = 1
        new.create_time = now
        new.update_time = now
        db_session.add(new)
        db_session.commit()
        news = get_news_by_key(str(_key))
        if news is not None:
            _key = _key + str(new.id)
        new.key = _key
        db_session.commit()
        if int(_data) == 1:
            news_controller.news_template.delay()
        return new.to_dict()
    return None


def get_advertisement(id):
    with session_scope() as db_session:
        result = db_session.query(Advertisement).filter(
            Advertisement.id == id).all()
        if result is not None:
            return [results.to_dict() for results in result]
        return None
    return None


def list_advertisement(page, results_per_page, type=None):
    with session_scope() as db_session:
        support_columns = ("key", "title", "content",
                           "source_from", "source_url", "status")
        start = (page - 1) * results_per_page
        end = start + results_per_page
        query = db_session.query(Advertisement)
        _filter = None
        if type is not None:
            for item in support_columns:
                if item in type:
                    _symbol = type.get("op", 'op')
                    _type = type[item]
                    if symbol.get(_symbol, "=") == "like":
                        _type = "%" + ("%s" % (type[item])) + "%"
                    _filter = "`%s` %s '%s' " % (
                        item, symbol.get(_symbol, "="), _type)
        if _filter is not None:
            query = query.filter(text(_filter))
        count = query.count()
        results = query.order_by(
            Advertisement.publish_time.desc()).slice(start, end).all()
        return count, [info.to_dict() for info in results]
    return None


def update_advertisement(id, data):
    with session_scope() as db_session:
        now = int(time.time())
        result = db_session.query(Advertisement).filter(
            Advertisement.id == id).first()
        if result is None:
            return None
        support_columns = ("key", "title", "content", "image",
                           "color", "back_color", "publish_time", "url", "status")
        for column in support_columns:
            if column in data:
                setattr(result, column, data[column])
        result.publish_time = now
        result.update_time = now
        db_session.add(result)
        db_session.commit()
        return result.to_dict()
    return None


def create_advertisement(data):
    with session_scope() as db_session:
        # key = data.get("key", None)
        # if key is None:
        #     raise exceptions.KeyNeed()
        # advertisements = get_advertisement(key)
        # if advertisements is not None:
        #     raise exceptions.DuplicateKey()
        now = int(time.time())
        advertisement = Advertisement()
        advertisement.set_create_table_base()
        support_columns = ("key", "title", "content", "image",
                           "color", "back_color", "publish_time", "url", "status")
        for column in support_columns:
            if column in data:
                setattr(advertisement, column, data[column])
        advertisement.create_time = now
        advertisement.update_time = now
        db_session.add(advertisement)
        db_session.commit()
        return advertisement.to_dict()
    return None


def delete_advertisement(id):
    with session_scope() as db_session:
        db_session.query(Advertisement).filter(
            Advertisement.id == id).delete(False)
        db_session.commit()
        return True
    return None
