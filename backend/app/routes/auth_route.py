from flask import Blueprint, request, jsonify, current_app, url_for
from ..extensions import jwt
from ..sqls.auth_sql import (
    get_user_by_account,
    exists_user,
    create_user,
    update_password,
    get_user_by_id,
    update_user_profile,
)
from ..utils.helpers import allowed_file, save_upload_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname')

    if exists_user(username=username):
        return jsonify({
            'code': 400,
            'message': '用户名已存在',
            'data':False
        })

    user = create_user(username=username, password=password, nickname=nickname)
    return jsonify({
        'code': 200,
        'message': '注册成功',
        'data': True
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_account(username)
    if not user or not user.check_password(password):
        return jsonify({
            'code': 400,
            'message': '用户名或密码错误',
            'data': False
        })

    access_token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(hours=2))
    return jsonify({
        'code': 200,
        'message': '登录成功',
        'data': {
            'token': access_token,
            'user_info': user.to_dict() if hasattr(user, 'to_dict') else {}
        }
    })

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """退出登录 - 前端移除token即可"""
    return jsonify({
        'code': 200,
        'message': '退出成功',
        'data': True
    })

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not user.check_password(old_password):
        return jsonify({
            'code': 400,
            'message': '原密码错误',
            'data': False
        })

    if new_password != confirm_password:
        return jsonify({
            'code': 400,
            'message': '两次密码不一致',
            'data': False
        })

    update_password(user, new_password)
    return jsonify({
        'code': 200,
        'message': '密码修改成功',
        'data': True
    })

@auth_bp.route('/user-info', methods=['GET'])
@jwt_required()
def user_info():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'code': 400,
            'message': '用户未找到',
            'data': None
        })

    user_data = {
        'user_id': user.user_id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'bio': user.bio,
        'campus': user.campus,
        'dormitory': user.dormitory,
        'credit_score': user.credit_score,
        'status': user.status,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat()
    }

    return jsonify({
        'code': 200,
        'message': '获取用户信息成功',
        'data': user_data
    })

@auth_bp.route('/update-profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    data = request.get_json()

    nickname = data.get('nickname')
    bio = data.get('bio')
    campus = data.get('campus')
    dormitory = data.get('dormitory')
    avatar = data.get('avatar')

    update_user_profile(user, nickname=nickname, bio=bio, campus=campus, dormitory=dormitory, avatar=avatar)

    return jsonify({
        'code': 200,
        'message': '用户信息更新成功',
        'data': True
    })

@auth_bp.route('/upload-avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({
            'code': 400,
            'message': '未上传文件',
            'data': False
        })

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'code': 400,
            'message': '未选择文件',
            'data': False
        })

    if not allowed_file(file.filename):
        return jsonify({
            'code': 400,
            'message': '文件格式不支持',
            'data': False
        }), 400

    # use helper to save and get URL
    avatar_url = save_upload_file(file, subdir='avatars')

    uid = int(get_jwt_identity())
    user = get_user_by_id(uid)
    if user:
        update_user_profile(user, avatar=avatar_url)

    return jsonify({
        'code': 200,
        'message': '头像上传成功',
        'data': {
            'avatar_url': avatar_url
        }
    })