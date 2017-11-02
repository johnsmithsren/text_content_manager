#!/usr/bin/env python
# coding=utf-8
"""News routes.

News routes
"""
from __future__ import unicode_literals

import time

from flask import session
from flask import request
from flask import jsonify
from flask import Blueprint

from content.controllers import news as news_controller
from content.utils import getLogger
from content.utils import exceptions

logger = getLogger(__name__)
news_bp = Blueprint("news", __name__)


@news_bp.route("", methods=["GET"])
def list_advertisement():
    """List news.

    @api {get} /new 获取广告列表
    @apiName ListNews
    @apiGroup News

    @apiParam {Number} page 页码。
    @apiParam {Number} results_per_page 每页显示的数量
    """
    page = 1
    results_per_page = 10
    try:
        page = int(request.args["page"])
    except:
        pass
    try:
        results_per_page = int(request.args["results_per_page"])
    except:
        pass
    count, data = news_controller.list_news(page, results_per_page)
    total_pages = count / \
        results_per_page if count % results_per_page == 0 else count / results_per_page + 1
    return jsonify({
        "code": 0,
        "data": {
            "objects": data,
            "total_pages": total_pages,
            "current_page": page,
            "num_results": count
        }
    })


@news_bp.route("/<key>", methods=["GET"])
def get(key):
    """Get news.

    @api {get} /news/:key 获取广告信息
    @apiName GetNews
    @apiGroup News
    """
    result = news_controller.get_news(key)
    if result is None:
        raise exceptions.GetNewsError()
    return jsonify({
        "code": 0,
        "data": result
    })


@news_bp.route("/test", methods=["GET"])
def test(key):
    """Get news
    """

    return jsonify({
        "code": 0,
        "data": result
    })
