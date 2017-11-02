#!/usr/bin/env python
# coding=utf-8
"""Entry of the program

Example:
python web.py start_dev --host 127.0.0.1 --port 5000 --wokers=1
"""
from __future__ import unicode_literals
import logging
import argparse
import logging.handlers
import sys
from gevent import monkey
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool


from content.app import app
from content.utils import getLogger
import werkzeug.serving

reload(sys)
sys.setdefaultencoding('utf-8')


def register_blueprints():
    from content.routes.news import news_bp
    from content.routes.advertisement import advertisement_bp
    app.register_blueprint(news_bp, url_prefix="/news")
    app.register_blueprint(advertisement_bp, url_prefix="/advertisement")


def db_sync():
    from content.models import entities
    from content.models import engine
    entities.Base.metadata.create_all(engine)


def start_dev(host="127.0.0.1", port=5000, workers=1):
    # werkzeug.serving.run_with_reloader()
    # register blueprints
    register_blueprints()
    # set debug mode
    app.debug = True

    @werkzeug.serving.run_with_reloader
    def run_server():
        "Start gevent WSGI server"
        monkey.patch_all()
        # use gevent WSGI server instead of the Flask
        http = WSGIServer((host, port), app.wsgi_app,
                          spawn=Pool(1), log=getLogger("wsgi"))
        # TODO gracefully handle shutdown
        http.serve_forever()

    run_server()


def start_rpc_server():
    logging.basicConfig(level=logging.INFO)
    from content.rpc import rpc_server
    rpc_server.start()


def start(host="127.0.0.1", port=5000, workers=1):
    register_blueprints()
    # set debug mode
    app.debug = False
    "Start gevent WSGI server"
    from gevent import monkey

    monkey.patch_all()
    # use gevent WSGI server instead of the Flask
    http = WSGIServer((host, port), app.wsgi_app,
                      spawn=Pool(workers), log=getLogger("wsgi"))
    # TODO gracefully handle shutdown
    http.serve_forever()


def start_generate_news():
    from content.utils import genenrate_news
    genenrate_news.news_template()


def start_generate_advertisement():
    from content.utils import generate_advertisement
    generate_advertisement.advertisement_template()


def main():
    parser = argparse.ArgumentParser(description='Start web server.')
    parser.add_argument('action', metavar='action', type=str,
                        help='start_dev or start')

    parser.add_argument('--host', dest='host',
                        default="127.0.0.1",
                        help='bind host(default: 127.0.0.1)')
    parser.add_argument('--port', dest='port', type=int,
                        default=5000,
                        help='bind port(default: 5000)')

    parser.add_argument('--workers', dest='workers', type=int,
                        default=1,
                        help='bind port(default: 5000)')
    args = parser.parse_args()
    if args.action == "start":
        start(args.host, args.port, args.workers)
    elif args.action == "start_dev":
        start_dev(args.host, args.port, args.workers)
    elif args.action == "start_rpc_server":
        start_rpc_server()
    elif args.action == "generate_news":
        start_generate_news()
    elif args.action == "generate_advertisement":
        start_generate_advertisement()
    elif args.action == 'db_sync':
        db_sync()


if __name__ == "__main__":
    main()
