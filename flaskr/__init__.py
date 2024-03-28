import os


from flask import Flask



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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
        return 'Hello, World!'

    from . import db
    db.init_db()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import fileupload
    app.register_blueprint(fileupload.bp)
    app.add_url_rule('/', endpoint='fileupload.index')

    app.config['S3_BUCKET'] = "project1s3imagesbucket"
    app.config['S3_KEY'] = "AKIAXCJY6ACWGBTNMSXF"
    app.config['S3_SECRET'] = "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"
    app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])

    return app
