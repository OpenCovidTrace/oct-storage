from sanic import Sanic, response

from gino.ext.sanic import Gino

from simple_settings import settings

from .web_exceptions import AppException

app = Sanic()
app.config.update(settings.as_dict())

db = Gino()
db.init_app(app)


async def server_error_handler(request, exc):
    data = {
        'data': exc.data,
        'message': exc.message,
        'message_code': exc.message_code,
        'message_human': exc.message_human
    }
    return response.json(data, status=exc.status_code)

app.error_handler.add(AppException, server_error_handler)

from . import views  # noqa
