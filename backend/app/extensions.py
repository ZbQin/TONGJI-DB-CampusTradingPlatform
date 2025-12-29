from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .utils.db_helper import init_db_helper


"""
初始化各类扩展
"""
jwt = JWTManager()

"""
绑定到应用实例
"""
def init_extensions(app):
    jwt.init_app(app)
    CORS(app, supports_credentials=True)
    init_db_helper(app)
