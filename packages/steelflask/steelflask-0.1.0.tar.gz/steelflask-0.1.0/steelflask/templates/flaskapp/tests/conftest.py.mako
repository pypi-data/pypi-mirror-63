
import pytest
from ${app_name}.app_factory import create_app
from tests.configuration import TestAppInitializer


@pytest.fixture(scope="session")
def app():
    app = create_app(AppInitializerClass=TestAppInitializer)
    return app


@pytest.fixture(scope="session")
def resource_uri(app):
    api_prefix = app.config['APPLICATION_ROOT']
    return {
        "ping": f"{api_prefix}/ping"
    }


@pytest.fixture()
def client(app):
    return app.test_client()
