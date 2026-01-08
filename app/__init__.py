from flask import Flask
from .extensions import db#, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    # login_manager.init_app(app)

    with app.app_context():
        # from .auth.routes import auth_bp
        # from .home.routes import home_bp
        # from .expense.routes import expense_bp

        db.create_all()

        # app.register_blueprint(auth_bp)
        # app.register_blueprint(home_bp)
        # app.register_blueprint(expense_bp, url_prefix='/expenses')

        return app
