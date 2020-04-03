from sanic import Sanic, response

from gino.ext.sanic import Gino

import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration

from simple_settings import settings

from . import web_exceptions

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[SanicIntegration()],
        environment=settings.SENTRY_ENVIRONMENT,
        debug=settings.DEBUG
    )

app = Sanic(__name__)
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

app.error_handler.add(web_exceptions.AppException, server_error_handler)


@app.middleware('request')
async def auth_request(request):
    token = request.headers.get('X-API-Token')
    print(token)
    if not token or token != settings.SERVICE_TOKEN:
        raise web_exceptions.Unauthorized('need valid token')


from . import views  # noqa
