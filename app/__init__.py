from flask import Flask
import pymysql.cursors

def create_app():
    #Initialize the app from Flask
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True

    app.secret_key = 'some key that you will never guess'
    
    #Configure MySQL
    app.config['db'] = pymysql.connect(host='localhost',
                        user='root',
                        password='root',
                        unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                        database='flights_new',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

    from .blueprints.auth.auth import auth as auth_blueprint
    from .blueprints.auth.authStaff import auth as authStaff_blueprint
    from .blueprints.auth.authCust import auth as authCust_blueprint

    from .blueprints.main.main import main as main_blueprint
    from .blueprints.main.mainCust import main as mainCust_blueprint
    from .blueprints.main.mainStaff import main as mainStaff_blueprint

    from .blueprints.search.searchStaff import search as searchStaff_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(authStaff_blueprint)
    app.register_blueprint(authCust_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(mainCust_blueprint)
    app.register_blueprint(mainStaff_blueprint)
    app.register_blueprint(searchStaff_blueprint)

    return app
