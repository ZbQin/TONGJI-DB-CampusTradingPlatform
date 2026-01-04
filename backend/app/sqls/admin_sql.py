"""管理员和通知相关的 SQL 操作。"""
from typing import Optional, Dict, List
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


class AdminDict(dict):
    """管理员字典包装类。"""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'AdminDict' object has no attribute '{key}'")
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def check_password(self, password: str) -> bool:
        """验证密码（明文比较）。"""
        return self.get('password_hash', '') == password
    
    def to_dict(self) -> dict:
        """转换为字典。"""
        return {
            'admin_id': self.get('admin_id'),
            'username': self.get('username'),
            'role': self.get('role'),
            'status': self.get('status'),
            'last_login_time': self.get('last_login_time').strftime('%Y-%m-%d %H:%M:%S') if self.get('last_login_time') else None,
            'created_at': self.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if self.get('created_at') else None
        }


def get_admin_by_username(username: str) -> Optional[AdminDict]:
    """根据用户名查询管理员。"""
    sql = "SELECT * FROM admins WHERE username = %s LIMIT 1"
    with get_cursor() as cursor:
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
    return AdminDict(row) if row else None


def get_admin_by_id(admin_id: int) -> Optional[AdminDict]:
    """根据ID查询管理员。"""
    sql = "SELECT * FROM admins WHERE admin_id = %s LIMIT 1"
    with get_cursor() as cursor:
        cursor.execute(sql, (admin_id,))
        row = cursor.fetchone()
    return AdminDict(row) if row else None


def update_admin_login_time(admin_id: int) -> bool:
    """更新管理员最后登录时间。"""
    now = datetime.now(timezone.utc)
    sql = "UPDATE admins SET last_login_time = %s WHERE admin_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (now, admin_id))
        return cursor.rowcount > 0


def ban_user(user_id: int, admin_id: int, reason: str) -> bool:
    """封禁用户并发送通知。"""
    now = datetime.now(timezone.utc)
    # 更新用户状态为封禁
    ban_sql = "UPDATE user SET status = 0, updated_at = %s WHERE user_id = %s"
    # 创建通知
    notify_sql = """
        INSERT INTO notification (user_id, type, title, content, related_id, created_at)
        VALUES (%s, 1, '账户已被封禁', %s, %s, %s)
    """
    content = f"您的账户因违规已被封禁。原因：{reason}"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(ban_sql, (now, user_id))
        cursor.execute(notify_sql, (user_id, content, admin_id, now))
        return cursor.rowcount > 0


def unban_user(user_id: int, admin_id: int) -> bool:
    """解封用户并发送通知。"""
    now = datetime.now(timezone.utc)
    # 更新用户状态为正常
    unban_sql = "UPDATE user SET status = 1, updated_at = %s WHERE user_id = %s"
    # 创建通知
    notify_sql = """
        INSERT INTO notification (user_id, type, title, content, related_id, created_at)
        VALUES (%s, 1, '账户已解封', %s, %s, %s)
    """
    content = "您的账户已解封，可以正常使用。"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(unban_sql, (now, user_id))
        cursor.execute(notify_sql, (user_id, content, admin_id, now))
        return cursor.rowcount > 0


def create_notification(user_id: int, ntype: int, title: str, content: str, related_id: Optional[int] = None) -> int:
    """创建通知。"""
    now = datetime.now(timezone.utc)
    sql = """
        INSERT INTO notification (user_id, type, title, content, related_id, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (user_id, ntype, title, content, related_id, now))
        notification_id = cursor.lastrowid
    return notification_id


def get_user_notifications(user_id: int, page: int = 1, page_size: int = 20, is_read: Optional[int] = None) -> Dict:
    """查询用户的通知列表。"""
    offset = (page - 1) * page_size
    conditions = ["user_id = %s"]
    params = [user_id]
    
    if is_read is not None:
        conditions.append("is_read = %s")
        params.append(is_read)
    
    where_clause = " AND ".join(conditions)
    
    # 查询总数
    count_sql = f"SELECT COUNT(*) as total FROM notification WHERE {where_clause}"
    with get_cursor() as cursor:
        cursor.execute(count_sql, tuple(params))
        total = cursor.fetchone()['total']
    
    # 查询列表
    list_sql = f"""
        SELECT * FROM notification
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """
    params.extend([page_size, offset])
    with get_cursor() as cursor:
        cursor.execute(list_sql, tuple(params))
        rows = cursor.fetchall()
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': [dict(row) for row in rows] if rows else []
    }


def mark_notification_read(notification_id: int, user_id: int) -> bool:
    """标记通知为已读。"""
    sql = "UPDATE notification SET is_read = 1 WHERE notification_id = %s AND user_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (notification_id, user_id))
        return cursor.rowcount > 0


def mark_all_notifications_read(user_id: int) -> bool:
    """标记所有通知为已读。"""
    sql = "UPDATE notification SET is_read = 1 WHERE user_id = %s AND is_read = 0"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (user_id,))
        return cursor.rowcount > 0


def get_unread_count(user_id: int) -> int:
    """获取未读通知数量。"""
    sql = "SELECT COUNT(*) as count FROM notification WHERE user_id = %s AND is_read = 0"
    with get_cursor() as cursor:
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
    return row['count'] if row else 0
