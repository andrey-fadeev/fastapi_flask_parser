from pytest import fixture


def pytest_addoption(parser):
    parser.addoption("--port", action="store")


@fixture()
def port(request):
    port = request.config.getoption("--port")
    if port is None:
        port = 8000
    return port
