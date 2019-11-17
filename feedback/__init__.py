import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'feeedback.sqlite'),
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
    @app.route('/')
    def hello():
        return render_template('feedback.html',
            name='Sally Student', ping_pct=95, streak=99, amount_earned=50,
            low_stress_me="socializing",
            low_stress_everyone="using the internet/apps",
            happiness_me="exercising",
            happiness_everyone="eating/drinking")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
