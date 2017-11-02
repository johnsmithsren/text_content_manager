#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

import callme

from content import config
from . import content_news

rpc_server = callme.Server(server_id='content_manager',
                           amqp_host=config['rpc']['amqp_host'],
                           amqp_user=config['rpc']['amqp_user'],
                           amqp_password=config['rpc']['amqp_password'],
                           amqp_vhost=config['rpc']['amqp_vhost'],
                           amqp_port=config['rpc']['amqp_port']
                           )

rpc_server.register_function(content_news.create_news, 'create_news')
rpc_server.register_function(content_news.get_news, "get_news")
rpc_server.register_function(content_news.update_news, "update_news")
rpc_server.register_function(content_news.list_news, "list_news")
rpc_server.register_function(content_news.delete_news, "delete_news")
rpc_server.register_function(content_news.list_advertisement, "list_advertisement")
rpc_server.register_function(content_news.get_advertisement, "get_advertisement")
rpc_server.register_function(content_news.create_advertisement, "create_advertisement")
rpc_server.register_function(content_news.delete_advertisement, "delete_advertisement")
rpc_server.register_function(content_news.update_advertisement, "update_advertisement")
