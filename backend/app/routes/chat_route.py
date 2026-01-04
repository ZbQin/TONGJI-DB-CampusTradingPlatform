from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import jwt
from ..sqls.chat_sql import (
    sql_get_session_list,
    sql_get_or_create_session,
    sql_get_message_list,
    sql_send_message,
    sql_mark_messages_read,
    sql_delete_session,
    sql_get_unread_count
)
from ..sqls.chat_sql import sql_get_user_by_id
from ..utils.helpers import allowed_file, save_upload_file

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@chat_bp.route('/session-list', methods=['GET'])
@jwt_required()
def get_session_list():
    """
    获取会话列表
    """
    user_id = int(get_jwt_identity())
    
    try:
        sessions = sql_get_session_list(user_id)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'list': sessions
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/get-or-create-session', methods=['POST'])
@jwt_required()
def get_or_create_session():
    """
    创建或获取会话
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    seller_id = data.get('seller_id')
    
    if not product_id or not seller_id:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数',
            'data': None
        })
    
    # 验证商品是否存在
    from ..utils.db_helper import get_cursor
    with get_cursor() as cursor:
        cursor.execute("SELECT product_id FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
    
    if not product:
        return jsonify({
            'code': 400,
            'message': '商品不存在',
            'data': None
        })
    
    try:
        session = sql_get_or_create_session(int(product_id), user_id, int(seller_id))
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': session
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'操作失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/message-list', methods=['GET'])
@jwt_required()
def get_message_list():
    """
    获取会话消息列表
    """
    user_id = int(get_jwt_identity())
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({
            'code': 400,
            'message': '缺少会话ID',
            'data': None
        })
    
    try:
        messages = sql_get_message_list(int(session_id), user_id)
        
        if messages is None:
            return jsonify({
                'code': 403,
                'message': '无权限查看该会话',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'list': messages
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/send-message', methods=['POST'])
@jwt_required()
def send_message():
    """
    发送消息
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    session_id = data.get('session_id')
    receiver_id = data.get('receiver_id')
    message_type = data.get('message_type')
    content = data.get('content')
    
    if not session_id or receiver_id is None or message_type is None or not content:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数',
            'data': None
        })
    
    if not content.strip():
        return jsonify({
            'code': 400,
            'message': '消息内容不能为空',
            'data': None
        })
    
    try:
        message = sql_send_message(
            int(session_id), 
            user_id, 
            int(receiver_id), 
            int(message_type), 
            content
        )
        
        if not message:
            return jsonify({
                'code': 403,
                'message': '无权限操作',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '发送成功',
            'data': message
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'发送失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/mark-read', methods=['POST'])
@jwt_required()
def mark_read():
    """
    标记消息为已读
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({
            'code': 400,
            'message': '缺少会话ID',
            'data': None
        })
    
    try:
        success = sql_mark_messages_read(int(session_id), user_id)
        
        if not success:
            return jsonify({
                'code': 403,
                'message': '无权限操作',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '标记成功',
            'data': True
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'操作失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    """
    上传聊天图片
    """
    if 'file' not in request.files:
        return jsonify({
            'code': 400,
            'message': '未找到文件',
            'data': None
        })
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'code': 400,
            'message': '文件名为空',
            'data': None
        })
    
    if not allowed_file(file.filename):
        return jsonify({
            'code': 400,
            'message': '文件格式不支持，仅支持jpg、png、jpeg、gif',
            'data': None
        })
    
    try:
        image_url = save_upload_file(file, 'chat')
        
        return jsonify({
            'code': 200,
            'message': '上传成功',
            'data': {
                'image_url': image_url
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'上传失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/delete-session', methods=['POST'])
@jwt_required()
def delete_session():
    """
    删除会话
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({
            'code': 400,
            'message': '缺少会话ID',
            'data': None
        })
    
    try:
        success = sql_delete_session(int(session_id), user_id)
        
        if not success:
            return jsonify({
                'code': 403,
                'message': '无权限删除该会话',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '删除成功',
            'data': True
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除失败: {str(e)}',
            'data': None
        })


@chat_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """
    获取未读消息数
    """
    user_id = int(get_jwt_identity())
    
    try:
        result = sql_get_unread_count(user_id)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}',
            'data': None
        })



@chat_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_info(user_id):
    """
    根据 user_id 返回昵称与头像，供前端按需查询
    """
    try:
        user = sql_get_user_by_id(user_id)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

        return jsonify({'code': 200, 'message': 'success', 'data': user})
    except Exception as e:
        return jsonify({'code': 500, 'message': f'查询失败: {str(e)}', 'data': None})
    