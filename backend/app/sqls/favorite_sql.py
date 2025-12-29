"""收藏相关的 SQL 操作"""
from typing import Dict, Optional
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


def sql_add_favorite(user_id: int, product_id: int) -> Optional[int]:
    """
    添加收藏
    :return: favorite_id 或 None（如果已收藏）
    """
    # 检查是否已收藏
    check_sql = "SELECT favorite_id FROM favorites WHERE user_id = %s AND product_id = %s"
    with get_cursor() as cursor:
        cursor.execute(check_sql, (user_id, product_id))
        existing = cursor.fetchone()
    
    if existing:
        return None
    
    # 添加收藏
    now = datetime.now(timezone.utc)
    insert_sql = "INSERT INTO favorites (user_id, product_id, created_at) VALUES (%s, %s, %s)"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(insert_sql, (user_id, product_id, now))
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        result = cursor.fetchone()
        favorite_id = result['id']
        
        # 更新商品收藏数
        cursor.execute("UPDATE product SET collect_count = collect_count + 1 WHERE product_id = %s", (product_id,))
    
    return favorite_id


def sql_cancel_favorite(user_id: int, product_id: int) -> bool:
    """
    取消收藏
    """
    delete_sql = "DELETE FROM favorites WHERE user_id = %s AND product_id = %s"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(delete_sql, (user_id, product_id))
        affected_rows = cursor.rowcount
        
        if affected_rows > 0:
            # 更新商品收藏数
            cursor.execute("UPDATE product SET collect_count = collect_count - 1 WHERE product_id = %s AND collect_count > 0", (product_id,))
            return True
    
    return False


def sql_get_my_favorites(user_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """
    获取我的收藏列表
    """
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM favorites WHERE user_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (user_id,))
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = """
        SELECT f.favorite_id, f.product_id, f.created_at,
               p.title, p.price, p.category_id, p.status,
               c.name as category_name,
               u.user_id as seller_id, u.nickname as seller_nickname, u.avatar as seller_avatar,
               (SELECT image_url FROM product_image WHERE product_id = p.product_id AND is_cover = 1 LIMIT 1) as cover_image
        FROM favorites f
        LEFT JOIN product p ON f.product_id = p.product_id
        LEFT JOIN user u ON p.user_id = u.user_id
        LEFT JOIN category c ON p.category_id = c.category_id
        WHERE f.user_id = %s
        ORDER BY f.created_at DESC
        LIMIT %s OFFSET %s
    """
    
    with get_cursor() as cursor:
        cursor.execute(list_sql, (user_id, page_size, offset))
        favorites = cursor.fetchall()
    
    # 格式化结果
    favorite_list = []
    for f in favorites or []:
        favorite_list.append({
            'favorite_id': f['favorite_id'],
            'product_id': f['product_id'],
            'title': f['title'],
            'price': float(f['price']) if f['price'] else 0,
            'category_id': f['category_id'],
            'category': f['category_name'],
            'status': f['status'],
            'images': [f['cover_image']] if f['cover_image'] else [],
            'seller': {
                'user_id': f['seller_id'],
                'nickname': f['seller_nickname'],
                'avatar': f['seller_avatar']
            },
            'created_at': f['created_at'].strftime('%Y-%m-%d %H:%M:%S') if f['created_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': favorite_list
    }


def sql_check_favorite(user_id: int, product_id: int) -> Dict:
    """
    检查是否收藏
    """
    check_sql = "SELECT favorite_id FROM favorites WHERE user_id = %s AND product_id = %s"
    
    with get_cursor() as cursor:
        cursor.execute(check_sql, (user_id, product_id))
        result = cursor.fetchone()
    
    if result:
        return {
            'is_favorited': True,
            'favorite_id': result['favorite_id']
        }
    else:
        return {
            'is_favorited': False,
            'favorite_id': None
        }
