#!/usr/bin/env python
# coding=utf-8
"""Entities for content

All database entities for content
"""
from __future__ import unicode_literals

import time

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import SMALLINT
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Unicode
from sqlalchemy import Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import CHAR
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseMixin:
    """Base Mixin for all entities.

    All common entities functions
    """

    def to_dict(self, exclude_columns=None):
        """Entity to dict.

        Entity to dict for all columns
        """
        if exclude_columns is None:
            exclude_columns = []
        d = {}
        for column in self.__table__.columns:
            if unicode(column.name) in exclude_columns:
                continue
            d[column.name] = getattr(self, column.name)

        return d


# 所有表公共字段
class TableBase:
    """Table base columns.

    Including columns like id, create time and update time
    """

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    create_time = Column(BigInteger)
    update_time = Column(BigInteger)

    def set_create_table_base(self):
        """Set base parameters for object.

        Set create / update time for object
        """
        now = int(time.time())
        self.create_time = now
        self.update_time = now

    def set_update_table_base(self):
        """Set base parameters for object update.

        Set update time for object
        """
        now = int(time.time())
        self.update_time = now


class News(Base, BaseMixin, TableBase):
    """News.

    News for content
    """

    __tablename__ = "news"
    key = Column(CHAR(128), unique=True, info="单独提供的key")
    title = Column(CHAR(128), info="新闻标题")
    content = Column(Text, info="新闻内容")
    source_from = Column(Text, info="新闻来源")
    source_url = Column(Text, info="新闻来源地址")
    publish_time = Column(BigInteger, info="发布时间")
    type = Column(CHAR(128), info="新闻类型")
    icon = Column(Text, info="图片")
    summary = Column(Text, info="摘要")
    status = Column(Integer)
    to_static = Column(Integer)


class Advertisement(Base, BaseMixin, TableBase):
    """Advertisement.

    Advertisement for content
    """

    __tablename__ = "advertisements"
    key = Column(CHAR(128), info="单独提供的key")
    title = Column(CHAR(128), info="广告标题")
    content = Column(Text, info="广告内容")
    image = Column(Text, info="图片地址")
    url = Column(Text, info="连接地址")
    color = Column(CHAR(128), nullable=True, info="广告颜色")
    back_color = Column(CHAR(128), nullable=True, info="背景颜色")
    type = Column(CHAR(128), nullable=True, info="新闻类型")
    publish_time = Column(BigInteger, info="发布时间")
    status = Column(Integer)
