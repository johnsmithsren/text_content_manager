#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

from codecs import open
from content.utils import exceptions
from content.models import session_scope
from content.models.entities import News
from content.models.entities import Advertisement
import time
import os
from flask import session
from flask import request
from flask import jsonify
from content.utils import templates
from flask import Blueprint
import shutil
from content.app import celery

_path = "/home/api/cloudcare-official-news"
# _path = "/Users/dzf/WebstormProjects/pythonproject/test"


def _set_time(time, format):
    res_time = ''
    if time is not None:
        time = int(time)
        res_time = utc_to_str(time, format)
    return res_time


def utc_to_str(num, format):
    if num is not None:
        v = int(num) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        return dt
    else:
        return


def create_news(data):
    _data = {
        "title": data.title,
        "content": data.content,
        "source_from": data.source_from,
        "create_time": _set_time(data.create_time, '%Y/%m/%d %H:%M'),
        "update_time": _set_time(data.update_time, '%Y/%m/%d %H:%M'),
        "source_url": data.source_url,
        "publish_time": _set_time(data.publish_time, '%Y/%m/%d %H:%M'),
        "summary": data.summary
    }

    path = "%s/news/detail/%s.html" % (_path, data.key)
    content = templates.render("detail.html", _data)
    f = open(path, "w+", encoding="utf8")
    f.write(content)
    f.close()


def create_list(summary):
    _path_ = _path + "/news/list"
    shutil.rmtree(_path_)
    os.mkdir(_path_)
    default_num = 10
    total_page = 0
    _info = []
    count = 0
    if len(summary) % default_num != 0:
        total_page = len(summary) / default_num + 1
    else:
        total_page = len(summary) / default_num
    for item in summary:
        item["time"] = _set_time(item["time"], '%Y/%m/%d %H:%M')
        _info.append(item)
        count = count + 1
        path = "%s/news/list/%s.html" % (_path, count / default_num)
        if (count % default_num) == 0:
            content = templates.render("news.html", {
                "attachments": _info,
                "current_page": (count / default_num),
                "total_page": total_page
            })
            _info = []
            f = open(path, "w+", encoding="utf8")
            f.write(content)
            f.close()
        if ((count == len(summary))):
            content = templates.render("news.html", {
                "attachments": _info,
                "current_page": total_page,
                "total_page": total_page
            })
            _info = []
            path = "%s/news/list/%s.html" % (_path, (count / default_num) + 1)
            f = open(path, "w+", encoding="utf8")
            f.write(content)
            f.close()


def create_page_one():
    now = int(time.time())
    _info = {
        "title": "标题暂无",
        "content": "内容暂无",
        "source_from": "来源暂无",
        "publish_time": _set_time(now, '%Y/%m/%d %H:%M')
    }
    content = templates.render("news.html", {
        "attachments": _info,
        "current_page": 1,
        "total_page": 1
    })
    f = open(path, "w+", encoding="utf8")
    f.write(content)
    f.close()


@celery.task
def news_template():
    with session_scope() as db_session:
        __path = _path + "/news/detail"
        shutil.rmtree(__path)
        os.mkdir(__path)
        now = int(time.time())
        _summary = []
        info = db_session.query(News).filter(
            News.status == 1).order_by(News.publish_time.desc()).all()
        for item in info:
            _path_ = _path + "/news/detail/%s.html" % item.key
            _result = os.path.exists(_path_)
            data = {
                "title": item.title or '',
                "summary": item.summary or '',
                "time": item.publish_time,
                "detail": "news/detail/%s.html" % item.key
            }
            create_news(item)
            _summary.append(data)
        if len(_summary) != 0:
            create_list(_summary)
        if not os.path.exists(_path + "/news/list/1.html"):
            create_page_one()
