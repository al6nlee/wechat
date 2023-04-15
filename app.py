# -*- coding: utf-8 -*-
# filename: main.py
import web
from src.handle.handle import Handle


urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
