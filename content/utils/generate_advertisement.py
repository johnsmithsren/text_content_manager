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


def create_advertisement(data):
    _data = {
        "key": data.key,
        "title": data.title,
        "content": data.content,
        "image": data.image,
        "color": data.color,
        "back_color": data.back_color,
        "publish_time": data.publish_time,
        "url": data.url,
        "create_time": data.create_time,
        "update_time": data.update_time
    }
    path = "./advertisement/%s.html" % data.key
    content = templates.render("advertisement.html", _data)
    f = open(path, "w+", encoding="utf8")
    f.write(content)
    f.close()


def create_advertisement_list(data):
    base_path = os.path.dirname(os.path.abspath(__file__))
    _path_ = base_path + "/../../advertisement/list"
    default_page = 5
    shutil.rmtree(_path_)
    os.mkdir(_path_)
    total_page = 0
    _info = []
    count = 0
    for item in summary:
        _info.append(item)
        count = count + 1
        if len(summary) % default_page != 0:
            total_page = len(summary) / default_page + 1
        else:
            total_page = len(summary) / default_page
        path = "./advertisement/list/page-%s.html" % (count / default_page - 1)
        if len(summary) < default_page:
            content = templates.render("advertisement.html", {
                "attachments": _info
            })
            _info = []
            f = open(path, "w+", encoding="utf8")
            f.write(content)
            f.close()
        if (count % default_page) == 0:
            content = templates.render("advertisement.html", {
                "attachments": _info
            })
            _info = []
            f = open(path, "w+", encoding="utf8")
            f.write(content)
            f.close()
        if ((count / default_page) == (total_page - 1) and (len(summary) % default_page != 0)):
            content = templates.render("advertisement.html", {
                "attachments": _info
            })
            _info = []
            path = "./advertisement/list/page-%s.html" % (total_page - 1)
            f = open(path, "w+", encoding="utf8")
            f.write(content)
            f.close()


def advertisement_template():
    with session_scope() as db_session:
        now = int(time.time())
        base_path = os.path.dirname(os.path.abspath(__file__))
        info = db_session.query(Advertisement).filter(
            Advertisement.status == 0).order_by(Advertisement.publish_time.desc()).all()
        for item in info:
            _path = base_path + "/../../advertisement/detail/%s.html" % item.key
            _result = os.path.exists(_path)
            data = {
                "title": item.title,
                "summary": item.summary,
                "time": item.publish_time,
                "detail": "http://120.27.135.41:85/api/v2/advertisement/%s" % item.key
            }
            if _result:
                create_time = os.path.getctime(_path)
                if (int(create_time) - int(item.publish_time)) > 0:
                    item.publish_time = now
                    db_session.commit()
                    os.remove(_path)
                    _summary.append(data)
                    create_advertisement(item)
            else:
                _summary.append(data)
                create_advertisement(item)
        if len(_summary) != 0:
            create_advertisement_list(_summary)
