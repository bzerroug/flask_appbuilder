from . import app


def debug():
    """ Launches the Flask debug server.
    """
    app.run(host='0.0.0.0', debug=True)
