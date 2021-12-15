import os

from flask import Flask, current_app


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev-2eaf2cb44ba465103e5a1f7953ea6c0ae1147a44511cf4ae050a811ea546f59a',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        print(current_app.config['DATABASE'])
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import application
    app.register_blueprint(application.bp)

    from . import api
    app.register_blueprint(api.bp)

    from . import counter
    app.register_blueprint(counter.bp)

    return app
