import os
import logging.config

from flask import Flask, Blueprint

from hbdeal.core.models import db
from hbdeal.core import hb_api


logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def register_views(app):
    from hbdeal.views import user, deals

    app.register_blueprint(user.bp)
    app.register_blueprint(deals.bp)


def initialize_app(settings_class=None):
    app = Flask(__name__)
    if settings_class is None:
        settings_class = os.getenv('HBDEAL_SETTING_CLASS', 'hbdeal.settings.DevSettings')

    app.config.from_object(settings_class)
    log.info(">>>>> Setting up app config from {}".format(settings_class))

    db.initialize_db(app)

    register_views(app)

    hb_api.appinit(app)

    return app


def main():
    app = initialize_app()
    log.info(('>>>>> Starting development server at http://{}/'
              .format(app.config['FLASK_SERVER_NAME'])))
    app.run()


if __name__ == "__main__":
    main()
