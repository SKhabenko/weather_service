import os

from aiohttp import web

import handlers


ROUTES = [
    web.get('/weather', handlers.Weather().get)
]


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(ROUTES)
    web.run_app(app, port=os.getenv('PORT', 8888))
