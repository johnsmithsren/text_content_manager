#!/usr/bin/env python
# coding=utf-8
"""Advertisement routes.

Advertisement routes
"""
from __future__ import unicode_literals

import time

from flask import session
from flask import request
from flask import jsonify
from flask import Blueprint

from content.controllers import advertisement as advertisement_controller
from content.utils import getLogger
from content.utils import exceptions

logger = getLogger(__name__)
advertisement_bp = Blueprint("advertisement", __name__)


@advertisement_bp.route("/<key>", methods=["GET"])
def get(key):
    """Get advertisement.

    @api {get} /advertisement/:id 获取广告信息
    @apiName GetAdvertisement
    @apiGroup Advertisement
    """
    result = advertisement_controller.get_advertisement(key)
    if result is None:
        raise exceptions.AdvertisementNotFound()
    return jsonify({
        "code": 0,
        "data": result
    })
