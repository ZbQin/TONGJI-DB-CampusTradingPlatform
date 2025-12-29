"""用户相关的 SQL 操作,使用原生 SQL 查询。"""
from typing import Optional, Dict
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


class UserDict(dict):
    """字典包装类，支持属性访问以保持向后兼容性。"""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'UserDict' object has no attribute '{key}'")
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def check_password(self, password: str) -> bool:
        """验证密码是否与存储的哈希值匹配。"""
        return self.get('password_hash', '') == password
    
    def to_dict(self) -> dict:
        """转换为普通字典用于 API 响应。"""
        return {
            'user_id': self.get('user_id'),
            'username': self.get('username'),
            'nickname': self.get('nickname'),
            'avatar': self.get('avatar'),
            'bio': self.get('bio'),
            'campus': self.get('campus'),
            'dormitory': self.get('dormitory'),
            'credit_score': self.get('credit_score', 100),
            'status': self.get('status', 1),
            'created_at': self.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if self.get('created_at') else None,
            'updated_at': self.get('updated_at').strftime('%Y-%m-%d %H:%M:%S') if self.get('updated_at') else None
        }


def get_user_by_account(account: str) -> Optional[UserDict]:
    """根据用户名查询用户。"""
    if not account:
        return None
    
    sql = "SELECT * FROM user WHERE username = %s LIMIT 1"
    with get_cursor() as cursor:
        cursor.execute(sql, (account,))
        row = cursor.fetchone()
    return UserDict(row) if row else None


def exists_user(username: str = None) -> bool:
    """检查用户名是否已存在。"""
    if not username:
        return False
    
    sql = "SELECT COUNT(*) as cnt FROM user WHERE username = %s"
    with get_cursor() as cursor:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
    return result['cnt'] > 0 if result else False


def create_user(username: str = None, password: str = None, nickname: str = None) -> UserDict:
    """向数据库插入新用户。"""
    password_hash = generate_password_hash(password)
    now = datetime.now(timezone.utc)
    
    sql = """
        INSERT INTO user (username, password_hash, nickname, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (username, password_hash, nickname, now, now))
        user_id = cursor.lastrowid
    
    # 返回新创建的用户
    return get_user_by_id(user_id)


def update_password(user: UserDict, new_password: str) -> None:
    """更新用户密码哈希值。"""
    password_hash = generate_password_hash(new_password)
    sql = "UPDATE user SET password_hash = %s, updated_at = %s WHERE user_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (password_hash, datetime.now(timezone.utc), user['user_id']))


def get_user_by_id(user_id: int) -> Optional[UserDict]:
    """根据用户 ID 查询用户。"""
    if not user_id:
        return None
    
    sql = "SELECT * FROM user WHERE user_id = %s LIMIT 1"
    with get_cursor() as cursor:
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
    return UserDict(row) if row else None


def update_user_profile(user: UserDict, **kwargs) -> None:
    """更新用户资料字段。"""
    allowed_fields = ['nickname', 'bio', 'campus', 'dormitory', 'avatar']
    updates = []
    params = []
    
    for field in allowed_fields:
        if field in kwargs and kwargs[field] is not None:
            updates.append(f"{field} = %s")
            params.append(kwargs[field])
    
    if not updates:
        return
    
    updates.append("updated_at = %s")
    params.append(datetime.now(timezone.utc))
    params.append(user['user_id'])
    
    sql = f"UPDATE user SET {', '.join(updates)} WHERE user_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, tuple(params))

def get_user_nicknameAndAvatar_by_id(user_id: int) -> Optional[Dict]:
    """根据用户 ID 查询用户昵称和头像。"""
    if not user_id:
        return None
    
    sql = "SELECT nickname, avatar FROM user WHERE user_id = %s LIMIT 1"
    with get_cursor() as cursor:
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
    if row:
        return {
            'nickname': row['nickname'],
            'avatar': row['avatar']
        }
    return None