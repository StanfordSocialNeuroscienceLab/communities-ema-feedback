import os

from flask import Flask, render_template, g

from feedback.auth import login_required


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        # DATABASE=os.path.join(app.instance_path, 'feeedback.sqlite'),
        # SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
        DATABASE_URL=os.environ['DATABASE_URL']
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

    @app.route('/')
    @login_required
    def index():
        common_activities = []
        for i in range(1, 4):
            col = 'common_activity_%d' % i
            if g.participant[col]:
                common_activities.append(g.participant[col])
        interaction_partners = []
        for i in range(1, 4):
            col = 'interaction_partner_%d' % i
            if g.participant[col]:
                interaction_partners.append(g.participant[col])
        return render_template('feedback.html',
            common_activities=common_activities,
            interaction_partners=interaction_partners)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

feedback_app = create_app()