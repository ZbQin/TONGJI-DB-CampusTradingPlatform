from flask import Flask, send_from_directory
import os
from .config import config_map
from .extensions import init_extensions

def create_app(config_name: str = 'default'):
    app = Flask(__name__, instance_relative_config=False)

    # 加载配置
    app.config.from_object(config_map.get(config_name, config_map['default']))

    # 初始化扩展
    init_extensions(app)

    # 注册路由蓝图（各 blueprint 内部已声明 url_prefix）
    from .routes.auth_route import auth_bp
    from .routes.product_route import product_bp
    from .routes.chat_route import chat_bp
    from .routes.category_route import category_bp
    from .routes.favorite_route import favorite_bp
    from .routes.follow_route import follow_bp
    from .routes.wanted_route import wanted_bp
    from .routes.review_route import review_bp
    from .routes.report_route import report_bp
    from .routes.admin_route import admin_bp, notification_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(follow_bp)
    app.register_blueprint(wanted_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notification_bp)

    # 配置静态文件服务
    @app.route('/static/uploads/<path:filename>')
    def serve_uploads(filename):
        """提供上传文件的静态访问"""
        uploads_dir = app.config.get('UPLOAD_FOLDER')
        return send_from_directory(uploads_dir, filename)

    # 健康检查
    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app
