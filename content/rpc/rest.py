#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

import json
import math

from sqlalchemy import inspect
from flask_restless.search import search as restless_search
from content.utils import exceptions


def session_query(session, model):
    if hasattr(model, 'query'):
        if callable(model.query):
            query = model.query()
        else:
            query = model.query
        if hasattr(query, 'filter'):
            return query
    return session.query(model)


def list_query_keys(model, exclude_columns=[]):
    mapper = inspect(model)
    query_keys = []

    for column in mapper.attrs:
        query_keys.append(column.key)

    if exclude_columns:
        for key in exclude_columns:
            query_keys.remove(key)

    return query_keys


def query(db_session, model, search_params={}, page=1, page_size=20, exclude_columns=['password']):
    if type(search_params) != type({}):
        raise exceptions.ParamsError()

    try:
        page = int(page)
        page_size = int(page_size)
    except Exception:
        raise exceptions.BadRequest()

    if page < 1:
        page = 1

    if page_size == 0 or page_size < -1:
        page_size = 20

    sort_key = model.id if hasattr(model, 'id') else None

    query_params = {}
    query_params['filters'] = search_params.get('filters', [])
    query_params['order_by'] = search_params.get('order_by', [])
    query_params['group_by'] = search_params.get('group_by', [])

    try:
        q = restless_search(db_session, model, query_params)
    except Exception:
        raise exceptions.BadRequest()

    if page_size == -1:
        total_pages = 1
        count = q.count()
        data = q.all()

    else:
        count = q.count()
        total_pages = int(math.ceil(count / float(page_size)))
        data = q.offset(page_size * page - page_size).limit(page_size).all()

    context = {}
    context['num_results'] = count
    context['objects'] = [item.to_dict(exclude_columns=exclude_columns) for item in data]
    context['page'] = page
    context['total_pages'] = total_pages

    return context


def get_model(instance):
    return type(instance)
