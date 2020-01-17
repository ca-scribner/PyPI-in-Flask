import os
import sys

import pytest

# I think pycharm handles this for us, but if it didn't we'd need...
# container_folder = os.path.dirname(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, container_folder)

import pypi_org.app
from pypi_org.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    # noinspection PyBroadException
    try:
        pypi_org.app.register_blueprints()
    except Exception as x:
        pass

    pypi_org.app.setup_db()

    yield client
