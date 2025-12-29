"""分类相关的路由"""
from flask import Blueprint, jsonify
from ..sqls.category_sql import sql_get_category_list

category_bp = Blueprint('category', __name__, url_prefix='/category')


@category_bp.route('/list', methods=['GET'])
def get_category_list():
    """
    获取分类列表
    """
    try:
        # 只返回启用状态的分类
        categories = sql_get_category_list(status=1)
        
        return jsonify({
            'code': 200,
            'message': '获取分类列表成功',
            'data': categories
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}',
            'data': None
        }), 500
