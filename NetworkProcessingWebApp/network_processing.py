from aiohttp import web

from NetworkProcessingDbLogic.db_controller import DbController
from NetworkProcessingWebApp.routes import setup_routes


def create_app():
    app = web.Application()
    setup_routes(app)
    dbcontroller = DbController(app)
    dbcontroller.init_app(app)
    return app


app = create_app()

if __name__ == "__main__":
    web.run_app(app)
