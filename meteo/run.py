from . import app


def debug():
    """ Launches the Flask debug server.
    """
    app.run(host='0.0.0.0', port=8080, debug=True)
