"""收藏相关路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..sqls.favorite_sql import (
    sql_add_favorite,
    sql_cancel_favorite,
    sql_get_my_favorites,
    sql_check_favorite
)

favorite_bp = Blueprint('favorite', __name__, url_prefix='/favorite')


@favorite_bp.route('/add', methods=['POST'])
@jwt_required()
def add_favorite():
    """添加收藏"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'code': 400, 'message': '商品ID不能为空'}), 400
    
    favorite_id = sql_add_favorite(current_user_id, product_id)
    
    if favorite_id is None:
        return jsonify({'code': 400, 'message': '该商品已收藏'}), 400
    
    return jsonify({
        'code': 200,
        'message': '收藏成功',
        'data': {'favorite_id': favorite_id}
    })


@favorite_bp.route('/cancel', methods=['POST'])
@jwt_required()
def cancel_favorite():
    """取消收藏"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'code': 400, 'message': '商品ID不能为空'}), 400
    
    success = sql_cancel_favorite(current_user_id, product_id)
    
    if not success:
        return jsonify({'code': 400, 'message': '取消收藏失败，未找到该收藏记录'}), 400
    
    return jsonify({
        'code': 200,
        'message': '取消收藏成功'
    })


@favorite_bp.route('/my-list', methods=['GET'])
@jwt_required()
def get_my_favorites():
    """获取我的收藏列表"""
    current_user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = sql_get_my_favorites(current_user_id, page, page_size)
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })


@favorite_bp.route('/check', methods=['GET'])
@jwt_required()
def check_favorite():
    """检查是否收藏"""
    current_user_id = int(get_jwt_identity())
    
    product_id = request.args.get('product_id', type=int)
    
    if not product_id:
        return jsonify({'code': 400, 'message': '商品ID不能为空'}), 400
    
    result = sql_check_favorite(current_user_id, product_id)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': result
    })
