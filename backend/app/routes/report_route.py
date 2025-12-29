"""举报路由。"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..sqls.report_sql import (
    create_report,
    get_report_by_id,
    get_report_list,
    get_my_reports,
    handle_report,
    delete_report
)

report_bp = Blueprint('report', __name__, url_prefix='/report')


@report_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    """创建举报。"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    reported_id = data.get('reported_id')
    target_type = data.get('target_type')  # 0-商品 1-用户
    target_id = data.get('target_id')
    reason = data.get('reason')
    description = data.get('description', '')
    
    if target_type is None or not target_id or not reason:
        return jsonify({'code': 400, 'message': '举报对象类型、对象ID和举报原因不能为空', 'data': None})
    
    if target_type not in [0, 1]:
        return jsonify({'code': 400, 'message': '举报对象类型错误', 'data': None})
    
    report_id = create_report(user_id, reported_id, target_type, target_id, reason, description)
    
    return jsonify({
        'code': 200,
        'message': '举报成功',
        'data': {'report_id': report_id}
    })


@report_bp.route('/detail/<int:report_id>', methods=['GET'])
@jwt_required()
def detail(report_id):
    """获取举报详情。"""
    report = get_report_by_id(report_id)
    if not report:
        return jsonify({'code': 404, 'message': '举报不存在', 'data': None})
    
    return jsonify({'code': 200, 'message': 'success', 'data': report})


@report_bp.route('/my-list', methods=['GET'])
@jwt_required()
def my_list():
    """获取我的举报列表。"""
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = get_my_reports(user_id, page, page_size)
    return jsonify({'code': 200, 'message': 'success', 'data': result})


@report_bp.route('/list', methods=['GET'])
@jwt_required()
def list_all():
    """获取举报列表（管理员）。"""
    # 注：实际应检查管理员权限，此处简化
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    status = request.args.get('status', type=int)
    target_type = request.args.get('target_type', type=int)
    
    result = get_report_list(page, page_size, status, target_type)
    return jsonify({'code': 200, 'message': 'success', 'data': result})


@report_bp.route('/handle/<int:report_id>', methods=['POST'])
@jwt_required()
def handle(report_id):
    """处理举报（管理员）。"""
    # 注：实际应检查管理员权限，此处简化
    admin_id = int(get_jwt_identity())
    data = request.get_json()
    
    status = data.get('status')  # 1-已处理 2-已驳回
    handle_result = data.get('handle_result', '')
    
    if status not in [1, 2]:
        return jsonify({'code': 400, 'message': '处理状态错误', 'data': None})
    
    report = get_report_by_id(report_id)
    if not report:
        return jsonify({'code': 404, 'message': '举报不存在', 'data': None})
    
    success = handle_report(report_id, admin_id, status, handle_result)
    if success:
        return jsonify({'code': 200, 'message': '处理成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '处理失败', 'data': False})


@report_bp.route('/delete/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete(report_id):
    """删除举报（管理员）。"""
    # 注：实际应检查管理员权限，此处简化
    success = delete_report(report_id)
    if success:
        return jsonify({'code': 200, 'message': '删除成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '删除失败', 'data': False})
