from oct_storage import app
from simple_settings import settings


if __name__ == '__main__':
    app.run(debug=True, host=settings.HOST)
