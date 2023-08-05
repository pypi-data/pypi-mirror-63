from ${app_name}.app_factory import AppInitializer

TEST_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': '${app_name}_test'
}

testConfiguration = {
    'SQLALCHEMY_DATABASE_URI': 'postgresql+psycopg2://{host}:{port}/{database}'.format(**TEST_DB_CONFIG),
    'SQLALCHEMY_ECHO': False,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'TESTING': True
}


class TestAppInitializer(AppInitializer):
    def load_configurations(self):
        super(TestAppInitializer, self).load_configurations()
        self.flask_app.config.from_mapping(testConfiguration)
