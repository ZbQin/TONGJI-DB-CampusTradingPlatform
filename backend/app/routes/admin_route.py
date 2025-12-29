"""管理员和通知路由。"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from ..sqls.admin_sql import (
    get_admin_by_username,
    get_admin_by_id,
    update_admin_login_time,
    ban_user,
    unban_user,
    create_notification,
    get_user_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    get_unread_count
)
from ..sqls.auth_sql import get_user_by_id

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['POST'])
def login():
    """管理员登录。"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    admin = get_admin_by_username(username)
    if not admin or not admin.check_password(password):
        return jsonify({'code': 400, 'message': '用户名或密码错误', 'data': None})
    
    if admin.get('status') != 1:
        return jsonify({'code': 403, 'message': '账户已被禁用', 'data': None})
    
    # 更新登录时间
    update_admin_login_time(admin['admin_id'])
    
    # 生成token（admin_id前加 'admin_' 前缀以区分）
    access_token = create_access_token(identity=f"admin_{admin['admin_id']}", expires_delta=timedelta(hours=8))
    
    return jsonify({
        'code': 200,
        'message': '登录成功',
        'data': {
            'token': access_token,
            'admin_info': admin.to_dict()
        }
    })


@admin_bp.route('/ban-user/<int:user_id>', methods=['POST'])
@jwt_required()
def ban_user_account(user_id):
    """封禁用户。"""
    identity = get_jwt_identity()
    if not identity.startswith('admin_'):
        return jsonify({'code': 403, 'message': '无权限', 'data': None})
    
    admin_id = int(identity.replace('admin_', ''))
    data = request.get_json()
    reason = data.get('reason', '违反平台规定')
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})
    
    success = ban_user(user_id, admin_id, reason)
    if success:
        return jsonify({'code': 200, 'message': '封禁成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '封禁失败', 'data': False})


@admin_bp.route('/unban-user/<int:user_id>', methods=['POST'])
@jwt_required()
def unban_user_account(user_id):
    """解封用户。"""
    identity = get_jwt_identity()
    if not identity.startswith('admin_'):
        return jsonify({'code': 403, 'message': '无权限', 'data': None})
    
    admin_id = int(identity.replace('admin_', ''))
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})
    
    success = unban_user(user_id, admin_id)
    if success:
        return jsonify({'code': 200, 'message': '解封成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '解封失败', 'data': False})


@admin_bp.route('/send-notification', methods=['POST'])
@jwt_required()
def send_notification():
    """管理员发送通知给用户。"""
    identity = get_jwt_identity()
    if not identity.startswith('admin_'):
        return jsonify({'code': 403, 'message': '无权限', 'data': None})
    
    data = request.get_json()
    user_id = data.get('user_id')
    ntype = data.get('type', 0)
    title = data.get('title')
    content = data.get('content')
    related_id = data.get('related_id')
    
    if not user_id or not title or not content:
        return jsonify({'code': 400, 'message': '用户ID、标题和内容不能为空', 'data': None})
    
    notification_id = create_notification(user_id, ntype, title, content, related_id)
    
    return jsonify({
        'code': 200,
        'message': '通知发送成功',
        'data': {'notification_id': notification_id}
    })


# 用户通知相关接口（普通用户也可使用）
notification_bp = Blueprint('notification', __name__, url_prefix='/notification')


@notification_bp.route('/list', methods=['GET'])
@jwt_required()
def list_notifications():
    """获取当前用户的通知列表。"""
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    is_read = request.args.get('is_read', type=int)
    
    result = get_user_notifications(user_id, page, page_size, is_read)
    return jsonify({'code': 200, 'message': 'success', 'data': result})


@notification_bp.route('/mark-read/<int:notification_id>', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    """标记通知为已读。"""
    user_id = int(get_jwt_identity())
    success = mark_notification_read(notification_id, user_id)
    if success:
        return jsonify({'code': 200, 'message': '标记成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '标记失败', 'data': False})


@notification_bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_read():
    """标记所有通知为已读。"""
    user_id = int(get_jwt_identity())
    success = mark_all_notifications_read(user_id)
    if success:
        return jsonify({'code': 200, 'message': '标记成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '标记失败', 'data': False})


@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def unread_count():
    """获取未读通知数量。"""
    user_id = int(get_jwt_identity())
    count = get_unread_count(user_id)
    return jsonify({'code': 200, 'message': 'success', 'data': {'count': count}})
