"""关注相关路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..sqls.follow_sql import (
    sql_follow_user,
    sql_unfollow_user,
    sql_get_following,
    sql_get_followers,
    sql_check_following,
    sql_get_follow_stats
)

follow_bp = Blueprint('follow', __name__, url_prefix='/follow')


@follow_bp.route('/add', methods=['POST'])
@jwt_required()
def follow_user():
    """关注用户"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    followee_id = data.get('user_id')
    
    if not followee_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400
    
    if current_user_id == followee_id:
        return jsonify({'code': 400, 'message': '不能关注自己'}), 400
    
    follow_id = sql_follow_user(current_user_id, followee_id)
    
    if follow_id is None:
        return jsonify({'code': 400, 'message': '已关注该用户'}), 400
    
    return jsonify({
        'code': 200,
        'message': '关注成功',
        'data': {'follow_id': follow_id}
    })


@follow_bp.route('/cancel', methods=['POST'])
@jwt_required()
def unfollow_user():
    """取消关注"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    followee_id = data.get('user_id')
    
    if not followee_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400
    
    success = sql_unfollow_user(current_user_id, followee_id)
    
    if not success:
        return jsonify({'code': 400, 'message': '取消关注失败，未找到关注记录'}), 400
    
    return jsonify({
        'code': 200,
        'message': '取消关注成功'
    })


@follow_bp.route('/following', methods=['GET'])
@jwt_required()
def get_following():
    """获取关注列表（我关注的人）"""
    current_user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = sql_get_following(current_user_id, page, page_size)
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })


@follow_bp.route('/followers', methods=['GET'])
@jwt_required()
def get_followers():
    """获取粉丝列表（关注我的人）"""
    current_user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = sql_get_followers(current_user_id, page, page_size)
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })


@follow_bp.route('/check', methods=['GET'])
@jwt_required()
def check_following():
    """检查是否关注某用户"""
    current_user_id = int(get_jwt_identity())
    
    followee_id = request.args.get('user_id', type=int)
    
    if not followee_id:
        return jsonify({'code': 400, 'message': '用户ID不能为空'}), 400
    
    result = sql_check_following(current_user_id, followee_id)
    
    return jsonify({
        'code': 200,
        'message': '查询成功',
        'data': result
    })


@follow_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_follow_stats():
    """获取关注统计"""
    current_user_id = int(get_jwt_identity())
    
    # 可选：查询其他用户的统计
    user_id = request.args.get('user_id', current_user_id, type=int)
    
    result = sql_get_follow_stats(user_id)
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })
