from flask import Flask
from flask_cors import CORS
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 使用 routes/__init__.py 中定义的路由
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 