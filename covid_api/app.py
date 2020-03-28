from sanic import Sanic

from gino.ext.sanic import Gino

from simple_settings import settings

app = Sanic()
app.config.update(settings.as_dict())

db = Gino()
db.init_app(app)


from . import views  # noqa
