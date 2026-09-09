from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
# from api.routes import register_routes
from api.swagger import spec
from api.controllers.todo_controller import bp as todo_bp
from api.controllers.auth_controller import auth_bp as auth_bp
# 1. IMPORT CONTROLLER MỚI Ở ĐÂY
from api.controllers.submission_controller import bp as submission_bp 

from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    Swagger(app)
    
    # Đăng ký blueprint trước
    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)
    # 2. ĐĂNG KÝ ROUTER MỚI Ở ĐÂY
    app.register_blueprint(submission_bp) 

    # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Film Photography Contest API"} # Cập nhật lại tên cho ngầu :D
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Register middleware
    middleware(app)

    # Register routes
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            # 3. THÊM 'submissions.' VÀO ĐÂY ĐỂ API HIỆN LÊN TRANG /docs
            if rule.endpoint.startswith(('todo.', 'course.', 'user.', 'auth.', 'submissions.')):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)
            
    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9999, debug=True)