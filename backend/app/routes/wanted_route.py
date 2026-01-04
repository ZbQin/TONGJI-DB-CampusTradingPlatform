"""求购相关路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..sqls.wanted_sql import (
    sql_publish_wanted,
    sql_get_wanted_list,
    sql_get_wanted_detail,
    sql_get_my_wanted,
    sql_update_wanted_status,
    sql_delete_wanted
)

wanted_bp = Blueprint('wanted', __name__, url_prefix='/wanted')


@wanted_bp.route('/publish', methods=['POST'])
@jwt_required()
def publish_wanted():
    """发布求购"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    category_id = data.get('category_id')
    expected_price = data.get('expected_price')
    
    # 验证必填字段
    if not title:
        return jsonify({'code': 400, 'message': '标题不能为空'}), 400
    if not description:
        return jsonify({'code': 400, 'message': '描述不能为空'}), 400
    if not category_id:
        return jsonify({'code': 400, 'message': '分类不能为空'}), 400
    if expected_price is None or expected_price < 0:
        return jsonify({'code': 400, 'message': '期望价格必须大于等于0'}), 400
    
    wanted_id = sql_publish_wanted(
        user_id=current_user_id,
        title=title,
        description=description,
        category_id=category_id,
        expected_price=expected_price
    )
    
    return jsonify({
        'code': 200,
        'message': '发布成功',
        'data': {'wanted_id': wanted_id}
    })


@wanted_bp.route('/list', methods=['GET'])
def get_wanted_list():
    """获取求购列表"""
    category_id = request.args.get('category_id', type=int)
    status = request.args.get('status', 0, type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    # 验证状态值
    if status not in [0, 1, 2]:
        status = 0
    
    result = sql_get_wanted_list(
        category_id=category_id,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })


@wanted_bp.route('/detail', methods=['GET'])
def get_wanted_detail():
    """获取求购详情"""
    wanted_id = request.args.get('wanted_id', type=int)
    
    if not wanted_id:
        return jsonify({'code': 400, 'message': '求购ID不能为空'}), 400
    
    detail = sql_get_wanted_detail(wanted_id)
    
    if not detail:
        return jsonify({'code': 404, 'message': '求购信息不存在'}), 404
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': detail
    })


@wanted_bp.route('/my-list', methods=['GET'])
@jwt_required()
def get_my_wanted():
    """获取我的求购列表"""
    current_user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = sql_get_my_wanted(current_user_id, page, page_size)
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': result
    })


@wanted_bp.route('/update-status', methods=['POST'])
@jwt_required()
def update_wanted_status():
    """更新求购状态"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    wanted_id = data.get('wanted_id')
    status = data.get('status')
    
    if not wanted_id:
        return jsonify({'code': 400, 'message': '求购ID不能为空'}), 400
    if status is None:
        return jsonify({'code': 400, 'message': '状态不能为空'}), 400
    if status not in [0, 1, 2]:
        return jsonify({'code': 400, 'message': '无效的状态值'}), 400
    
    success = sql_update_wanted_status(wanted_id, current_user_id, status)
    
    if not success:
        return jsonify({'code': 400, 'message': '更新失败，求购不存在或无权限'}), 400
    
    return jsonify({
        'code': 200,
        'message': '更新成功'
    })


@wanted_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_wanted():
    """删除求购"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    wanted_id = data.get('wanted_id')
    
    if not wanted_id:
        return jsonify({'code': 400, 'message': '求购ID不能为空'}), 400
    
    success = sql_delete_wanted(wanted_id, current_user_id)
    
    if not success:
        return jsonify({'code': 400, 'message': '删除失败，求购不存在或无权限'}), 400
    
    return jsonify({
        'code': 200,
        'message': '删除成功'
    })
