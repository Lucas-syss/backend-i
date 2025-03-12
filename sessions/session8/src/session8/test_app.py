from typer.testing import CliRunner
from app import app
import pytest


runner = CliRunner()

@pytest.fixture
def command():
    return runner.invoke(app=app,args=["3"])

def test_app(command):
    result = command
    assert "9" in result.stdout
