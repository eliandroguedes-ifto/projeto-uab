import pytest
import os
# Ensure environment variables are set BEFORE importing create_app if needed, 
# but create_app reads them when called.
os.environ['DATABASE_URI'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret'

from app import create_app, db
from app.models import Usuario

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
