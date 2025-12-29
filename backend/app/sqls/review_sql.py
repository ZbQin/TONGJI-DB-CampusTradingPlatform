"""评价相关的 SQL 操作。"""
from typing import Optional, List, Dict
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


def create_review(reviewer_id: int, reviewee_id: int, product_id: Optional[int], rating: int, content: str) -> int:
    """创建评价。"""
    now = datetime.now(timezone.utc)
    sql = """
        INSERT INTO reviews (reviewer_id, reviewee_id, product_id, rating, content, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (reviewer_id, reviewee_id, product_id, rating, content, now))
        review_id = cursor.lastrowid
    return review_id


def get_review_by_id(review_id: int) -> Optional[Dict]:
    """根据ID查询评价。"""
    sql = """
        SELECT r.*, 
               u1.nickname as reviewer_nickname, u1.avatar as reviewer_avatar,
               u2.nickname as reviewee_nickname, u2.avatar as reviewee_avatar,
               p.title as product_title
        FROM reviews r
        LEFT JOIN user u1 ON r.reviewer_id = u1.user_id
        LEFT JOIN user u2 ON r.reviewee_id = u2.user_id
        LEFT JOIN product p ON r.product_id = p.product_id
        WHERE r.review_id = %s
    """
    with get_cursor() as cursor:
        cursor.execute(sql, (review_id,))
        row = cursor.fetchone()
    return dict(row) if row else None


def get_reviews_by_reviewee(reviewee_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """查询用户收到的评价列表（被评价者）。"""
    offset = (page - 1) * page_size
    
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM reviews WHERE reviewee_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (reviewee_id,))
        total = cursor.fetchone()['total']
    
    # 查询列表
    list_sql = """
        SELECT r.*, 
               u1.nickname as reviewer_nickname, u1.avatar as reviewer_avatar,
               p.title as product_title
        FROM reviews r
        LEFT JOIN user u1 ON r.reviewer_id = u1.user_id
        LEFT JOIN product p ON r.product_id = p.product_id
        WHERE r.reviewee_id = %s
        ORDER BY r.created_at DESC
        LIMIT %s OFFSET %s
    """
    with get_cursor() as cursor:
        cursor.execute(list_sql, (reviewee_id, page_size, offset))
        rows = cursor.fetchall()
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': [dict(row) for row in rows] if rows else []
    }


def get_reviews_by_reviewer(reviewer_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """查询用户发出的评价列表（评价者）。"""
    offset = (page - 1) * page_size
    
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM reviews WHERE reviewer_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (reviewer_id,))
        total = cursor.fetchone()['total']
    
    # 查询列表
    list_sql = """
        SELECT r.*, 
               u2.nickname as reviewee_nickname, u2.avatar as reviewee_avatar,
               p.title as product_title
        FROM reviews r
        LEFT JOIN user u2 ON r.reviewee_id = u2.user_id
        LEFT JOIN product p ON r.product_id = p.product_id
        WHERE r.reviewer_id = %s
        ORDER BY r.created_at DESC
        LIMIT %s OFFSET %s
    """
    with get_cursor() as cursor:
        cursor.execute(list_sql, (reviewer_id, page_size, offset))
        rows = cursor.fetchall()
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': [dict(row) for row in rows] if rows else []
    }


def get_user_rating_stats(user_id: int) -> Dict:
    """获取用户的评分统计。"""
    sql = """
        SELECT 
            COUNT(*) as review_count,
            IFNULL(AVG(rating), 0) as avg_rating
        FROM reviews
        WHERE reviewee_id = %s
    """
    with get_cursor() as cursor:
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
    return dict(row) if row else {'review_count': 0, 'avg_rating': 0}


def delete_review(review_id: int) -> bool:
    """删除评价（仅限评价者本人或管理员）。"""
    sql = "DELETE FROM reviews WHERE review_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (review_id,))
        return cursor.rowcount > 0
