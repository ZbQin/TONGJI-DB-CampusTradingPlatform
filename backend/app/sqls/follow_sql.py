"""关注相关的 SQL 操作"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


def sql_follow_user(follower_id: int, followee_id: int) -> Optional[int]:
    """
    关注用户
    :return: follow_id 或 None（如果已关注或关注自己）
    """
    # 不能关注自己
    if follower_id == followee_id:
        return None
    
    # 检查是否已关注
    check_sql = "SELECT follow_id FROM follows WHERE follower_id = %s AND followee_id = %s"
    with get_cursor() as cursor:
        cursor.execute(check_sql, (follower_id, followee_id))
        existing = cursor.fetchone()
    
    if existing:
        return None
    
    # 添加关注
    now = datetime.now(timezone.utc)
    insert_sql = "INSERT INTO follows (follower_id, followee_id, created_at) VALUES (%s, %s, %s)"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(insert_sql, (follower_id, followee_id, now))
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        result = cursor.fetchone()
        follow_id = result['id']
    
    return follow_id


def sql_unfollow_user(follower_id: int, followee_id: int) -> bool:
    """
    取消关注
    """
    delete_sql = "DELETE FROM follows WHERE follower_id = %s AND followee_id = %s"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(delete_sql, (follower_id, followee_id))
        affected_rows = cursor.rowcount
    
    return affected_rows > 0


def sql_get_following(user_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """
    获取关注列表（我关注的人）
    """
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM follows WHERE follower_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (user_id,))
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = """
        SELECT f.follow_id, f.followee_id, f.created_at,
               u.nickname, u.avatar
        FROM follows f
        LEFT JOIN user u ON f.followee_id = u.user_id
        WHERE f.follower_id = %s
        ORDER BY f.created_at DESC
        LIMIT %s OFFSET %s
    """
    
    with get_cursor() as cursor:
        cursor.execute(list_sql, (user_id, page_size, offset))
        following = cursor.fetchall()
    
    # 格式化结果
    following_list = []
    for f in following or []:
        following_list.append({
            'follow_id': f['follow_id'],
            'user_id': f['followee_id'],
            'nickname': f['nickname'],
            'avatar': f['avatar'],
            'created_at': f['created_at'].strftime('%Y-%m-%d %H:%M:%S') if f['created_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': following_list
    }


def sql_get_followers(user_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """
    获取粉丝列表（关注我的人）
    """
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM follows WHERE followee_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (user_id,))
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = """
        SELECT f.follow_id, f.follower_id, f.created_at,
               u.nickname, u.avatar
        FROM follows f
        LEFT JOIN user u ON f.follower_id = u.user_id
        WHERE f.followee_id = %s
        ORDER BY f.created_at DESC
        LIMIT %s OFFSET %s
    """
    
    with get_cursor() as cursor:
        cursor.execute(list_sql, (user_id, page_size, offset))
        followers = cursor.fetchall()
    
    # 格式化结果
    follower_list = []
    for f in followers or []:
        follower_list.append({
            'follow_id': f['follow_id'],
            'user_id': f['follower_id'],
            'nickname': f['nickname'],
            'avatar': f['avatar'],
            'created_at': f['created_at'].strftime('%Y-%m-%d %H:%M:%S') if f['created_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': follower_list
    }


def sql_check_following(follower_id: int, followee_id: int) -> Dict:
    """
    检查是否关注
    """
    check_sql = "SELECT follow_id FROM follows WHERE follower_id = %s AND followee_id = %s"
    
    with get_cursor() as cursor:
        cursor.execute(check_sql, (follower_id, followee_id))
        result = cursor.fetchone()
    
    if result:
        return {
            'is_following': True,
            'follow_id': result['follow_id']
        }
    else:
        return {
            'is_following': False,
            'follow_id': None
        }


def sql_get_follow_stats(user_id: int) -> Dict:
    """
    获取关注统计
    """
    stats_sql = """
        SELECT 
            (SELECT COUNT(*) FROM follows WHERE follower_id = %s) as following_count,
            (SELECT COUNT(*) FROM follows WHERE followee_id = %s) as followers_count
    """
    
    with get_cursor() as cursor:
        cursor.execute(stats_sql, (user_id, user_id))
        result = cursor.fetchone()
    
    return {
        'following_count': result['following_count'] if result else 0,
        'followers_count': result['followers_count'] if result else 0
    }
