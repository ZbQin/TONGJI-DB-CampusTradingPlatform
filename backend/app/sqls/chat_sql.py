from ..utils.db_helper import get_cursor
from datetime import datetime, timezone


def sql_get_session_list(user_id: int) -> list:
    """
    获取用户的聊天会话列表
    """
    query = """
    SELECT cs.session_id, cs.buyer_id, cs.seller_id, cs.last_message, cs.updated_at
    FROM chat_session cs
    WHERE cs.buyer_id = %s OR cs.seller_id = %s
    ORDER BY cs.updated_at DESC
    """
    
    with get_cursor() as cursor:
        cursor.execute(query, (user_id, user_id))
        results = cursor.fetchall()
    
    chat_sessions = []
    for row in results:
        # 计算该会话的未读消息数
        with get_cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as unread_count
                FROM chat_message cm
                WHERE cm.session_id = %s AND cm.receiver_id = %s AND cm.is_read = 0
            """, (row['session_id'], user_id))
            unread_result = cursor.fetchone()
        
        chat_sessions.append({
            'session_id': row['session_id'],
            'buyer_id': row['buyer_id'],
            'seller_id': row['seller_id'],
            'last_message': row['last_message'],
            'updated_at': row['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if row['updated_at'] else None,
            'unread_count': unread_result['unread_count'] if unread_result else 0
        })
    return chat_sessions


def sql_get_or_create_session(product_id: int, buyer_id: int, seller_id: int) -> dict:
    """
    创建或获取会话
    """
    # 先查询会话是否存在
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT session_id, product_id, buyer_id, seller_id, created_at
            FROM chat_session
            WHERE product_id = %s AND buyer_id = %s AND seller_id = %s
            LIMIT 1
        """, (product_id, buyer_id, seller_id))
        session = cursor.fetchone()
    
    if session:
        return {
            'session_id': session['session_id'],
            'product_id': session['product_id'],
            'buyer_id': session['buyer_id'],
            'seller_id': session['seller_id'],
            'created_at': session['created_at'].strftime('%Y-%m-%d %H:%M:%S') if session['created_at'] else None
        }
    
    # 创建新会话
    now = datetime.now(timezone.utc)
    with get_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO chat_session (product_id, buyer_id, seller_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (product_id, buyer_id, seller_id, now, now))
        session_id = cursor.lastrowid
    
    return {
        'session_id': session_id,
        'product_id': product_id,
        'buyer_id': buyer_id,
        'seller_id': seller_id,
        'created_at': now.strftime('%Y-%m-%d %H:%M:%S')
    }


def sql_get_message_list(session_id: int, user_id: int) -> list:
    """
    获取会话消息列表
    """
    # 验证用户是否是会话参与者
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT buyer_id, seller_id
            FROM chat_session
            WHERE session_id = %s
        """, (session_id,))
        session = cursor.fetchone()
    
    if not session:
        return None
    
    if user_id not in [session['buyer_id'], session['seller_id']]:
        return None
    
    # 查询消息列表
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT message_id, session_id, sender_id, receiver_id, 
                   message_type, content, is_read, created_at
            FROM chat_message
            WHERE session_id = %s
            ORDER BY created_at ASC
        """, (session_id,))
        messages = cursor.fetchall()
    
    message_list = []
    for msg in messages or []:
        message_list.append({
            'message_id': msg['message_id'],
            'session_id': msg['session_id'],
            'sender_id': msg['sender_id'],
            'receiver_id': msg['receiver_id'],
            'message_type': msg['message_type'],
            'content': msg['content'],
            'is_read': msg['is_read'],
            'created_at': msg['created_at'].strftime('%Y-%m-%d %H:%M:%S') if msg['created_at'] else None
        })
    return message_list


def sql_send_message(session_id: int, sender_id: int, receiver_id: int, 
                     message_type: int, content: str) -> dict:
    """
    发送消息
    """
    # 验证发送者是否是会话参与者
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT buyer_id, seller_id
            FROM chat_session
            WHERE session_id = %s
        """, (session_id,))
        session = cursor.fetchone()
    
    if not session:
        return None
    
    if sender_id not in [session['buyer_id'], session['seller_id']]:
        return None
    
    # 插入消息
    now = datetime.now(timezone.utc)
    with get_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO chat_message (session_id, sender_id, receiver_id, 
                                     message_type, content, is_read, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session_id, sender_id, receiver_id, message_type, content, 0, now))
        message_id = cursor.lastrowid
        
        # 更新会话的最后消息
        cursor.execute("""
            UPDATE chat_session
            SET last_message = %s, last_message_time = %s, updated_at = %s
            WHERE session_id = %s
        """, (content, now, now, session_id))
    
    return {
        'message_id': message_id,
        'session_id': session_id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message_type': message_type,
        'content': content,
        'is_read': 0,
        'created_at': now.strftime('%Y-%m-%d %H:%M:%S')
    }


def sql_mark_messages_read(session_id: int, user_id: int) -> bool:
    """
    标记会话中的消息为已读
    """
    # 验证用户是否是会话参与者
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT buyer_id, seller_id
            FROM chat_session
            WHERE session_id = %s
        """, (session_id,))
        session = cursor.fetchone()
    
    if not session:
        return False
    
    if user_id not in [session['buyer_id'], session['seller_id']]:
        return False
    
    # 标记该用户接收的未读消息为已读
    with get_cursor(commit=True) as cursor:
        cursor.execute("""
            UPDATE chat_message
            SET is_read = 1
            WHERE session_id = %s AND receiver_id = %s AND is_read = 0
        """, (session_id, user_id))
    
    return True


def sql_delete_session(session_id: int, user_id: int) -> bool:
    """
    删除会话
    """
    # 验证用户是否是会话参与者
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT buyer_id, seller_id
            FROM chat_session
            WHERE session_id = %s
        """, (session_id,))
        session = cursor.fetchone()
    
    if not session:
        return False
    
    if user_id not in [session['buyer_id'], session['seller_id']]:
        return False
    
    # 删除会话及相关消息
    with get_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM chat_message WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM chat_session WHERE session_id = %s", (session_id,))
    
    return True


def sql_get_unread_count(user_id: int) -> dict:
    """
    获取未读消息数统计
    """
    # 查询每个会话的未读消息数
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT cm.session_id, COUNT(*) as unread_count
            FROM chat_message cm
            JOIN chat_session cs ON cm.session_id = cs.session_id
            WHERE cm.receiver_id = %s AND cm.is_read = 0
              AND (cs.buyer_id = %s OR cs.seller_id = %s)
            GROUP BY cm.session_id
        """, (user_id, user_id, user_id))
        results = cursor.fetchall()
    
    sessions = []
    for row in results or []:
        sessions.append({
            'session_id': row['session_id'],
            'unread_count': row['unread_count']
        })
    
    return {'sessions': sessions}