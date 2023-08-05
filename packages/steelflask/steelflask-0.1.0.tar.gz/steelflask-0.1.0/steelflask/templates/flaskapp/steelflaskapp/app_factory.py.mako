# ${app_name}/app_factory.py
import os
from flask import Flask, jsonify
from ${app_name}.ext import db, migrate, APP_DIR
from ${app_name}.errorhandler import register_error_handlers
from ${app_name} import configuration
from ${app_name}.version import __version__


class AppInitializer:
    def __init__(self, app):
        self.flask_app = app

    def init_app(self):
        self.load_configurations()
        self.setup_db()
        register_error_handlers(self.flask_app)
        self.register_blueprints()

    def load_configurations(self):
        self.flask_app.config.from_object(configuration)

        cur_dir_config_file = os.path.join(os.getcwd(), "${app_name}_config.py")
        if os.path.exists(cur_dir_config_file) and os.path.isfile(cur_dir_config_file):
            self.flask_app.config.from_pyfile(cur_dir_config_file)

        config_module = os.environ.get("${app_name.upper()}_CONFIG")
        if config_module is not None:
            self.flask_app.config.from_object(config_module)

    def setup_db(self):
        db.init_app(self.flask_app)
        migrate.init_app(self.flask_app, db=db, directory=APP_DIR + "/migrations")

    def register_blueprints(self):
        pass


def create_app(AppInitializerClass=AppInitializer):
    app = Flask('${app_name}', static_folder='static', static_url_path='/')
    app_initializer = AppInitializerClass(app)
    app_initializer.init_app()

    @app.route(f"{app.config['APPLICATION_ROOT']}/ping")
    def hello():
        return jsonify({
            'status': 'success',
            'alive': True,
            'version': __version__
        })
    return app
