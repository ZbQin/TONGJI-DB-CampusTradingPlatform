"""求购相关的 SQL 操作"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


def sql_publish_wanted(user_id: int, title: str, description: str, category_id: int, 
                       expected_price: float) -> int:
    """
    发布求购
    """
    now = datetime.now(timezone.utc)
    insert_sql = """
        INSERT INTO wanted (user_id, title, description, category_id, expected_price, 
                           status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, 0, %s, %s)
    """
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(insert_sql, (user_id, title, description, category_id, 
                                   expected_price, now, now))
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        result = cursor.fetchone()
        wanted_id = result['id']
    
    return wanted_id


def sql_get_wanted_list(category_id: Optional[int] = None, status: int = 0,
                        page: int = 1, page_size: int = 20) -> Dict:
    """
    获取求购列表
    """
    # 构建查询条件
    conditions = ["w.status = %s"]
    params = [status]
    
    if category_id:
        conditions.append("w.category_id = %s")
        params.append(category_id)
    
    where_clause = " AND ".join(conditions)
    
    # 查询总数
    count_sql = f"SELECT COUNT(*) as total FROM wanted w WHERE {where_clause}"
    with get_cursor() as cursor:
        cursor.execute(count_sql, params)
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = f"""
        SELECT w.wanted_id, w.title, w.description, w.category_id, w.expected_price,
               w.status, w.created_at, w.updated_at,
               c.name as category_name,
               u.user_id, u.nickname, u.avatar
        FROM wanted w
        LEFT JOIN user u ON w.user_id = u.user_id
        LEFT JOIN category c ON w.category_id = c.category_id
        WHERE {where_clause}
        ORDER BY w.created_at DESC
        LIMIT %s OFFSET %s
    """
    
    params.extend([page_size, offset])
    
    with get_cursor() as cursor:
        cursor.execute(list_sql, params)
        wanted_list = cursor.fetchall()
    
    # 格式化结果
    result_list = []
    for w in wanted_list or []:
        result_list.append({
            'wanted_id': w['wanted_id'],
            'title': w['title'],
            'description': w['description'],
            'category_id': w['category_id'],
            'category': w['category_name'],
            'expected_price': float(w['expected_price']) if w['expected_price'] else 0,
            'status': w['status'],
            'publisher': {
                'user_id': w['user_id'],
                'nickname': w['nickname'],
                'avatar': w['avatar']
            },
            'created_at': w['created_at'].strftime('%Y-%m-%d %H:%M:%S') if w['created_at'] else None,
            'updated_at': w['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if w['updated_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': result_list
    }


def sql_get_wanted_detail(wanted_id: int) -> Optional[Dict]:
    """
    获取求购详情
    """
    detail_sql = """
        SELECT w.wanted_id, w.user_id, w.title, w.description, w.category_id, 
               w.expected_price, w.status, w.created_at, w.updated_at,
               c.name as category_name,
               u.nickname, u.avatar
        FROM wanted w
        LEFT JOIN user u ON w.user_id = u.user_id
        LEFT JOIN category c ON w.category_id = c.category_id
        WHERE w.wanted_id = %s
    """
    
    with get_cursor() as cursor:
        cursor.execute(detail_sql, (wanted_id,))
        wanted = cursor.fetchone()
    
    if not wanted:
        return None
    
    return {
        'wanted_id': wanted['wanted_id'],
        'title': wanted['title'],
        'description': wanted['description'],
        'category_id': wanted['category_id'],
        'category': wanted['category_name'],
        'expected_price': float(wanted['expected_price']) if wanted['expected_price'] else 0,
        'status': wanted['status'],
        'publisher': {
            'user_id': wanted['user_id'],
            'nickname': wanted['nickname'],
            'avatar': wanted['avatar']
        },
        'created_at': wanted['created_at'].strftime('%Y-%m-%d %H:%M:%S') if wanted['created_at'] else None,
        'updated_at': wanted['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if wanted['updated_at'] else None
    }


def sql_get_my_wanted(user_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """
    获取我的求购列表
    """
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM wanted WHERE user_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (user_id,))
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = """
        SELECT w.wanted_id, w.title, w.description, w.category_id, w.expected_price,
               w.status, w.created_at, w.updated_at,
               c.name as category_name
        FROM wanted w
        LEFT JOIN category c ON w.category_id = c.category_id
        WHERE w.user_id = %s
        ORDER BY w.created_at DESC
        LIMIT %s OFFSET %s
    """
    
    with get_cursor() as cursor:
        cursor.execute(list_sql, (user_id, page_size, offset))
        wanted_list = cursor.fetchall()
    
    # 格式化结果
    result_list = []
    for w in wanted_list or []:
        result_list.append({
            'wanted_id': w['wanted_id'],
            'title': w['title'],
            'description': w['description'],
            'category_id': w['category_id'],
            'category': w['category_name'],
            'expected_price': float(w['expected_price']) if w['expected_price'] else 0,
            'status': w['status'],
            'created_at': w['created_at'].strftime('%Y-%m-%d %H:%M:%S') if w['created_at'] else None,
            'updated_at': w['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if w['updated_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': result_list
    }


def sql_update_wanted_status(wanted_id: int, user_id: int, status: int) -> bool:
    """
    更新求购状态（只能更新自己的）
    """
    now = datetime.now(timezone.utc)
    update_sql = """
        UPDATE wanted 
        SET status = %s, updated_at = %s 
        WHERE wanted_id = %s AND user_id = %s
    """
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(update_sql, (status, now, wanted_id, user_id))
        affected_rows = cursor.rowcount
    
    return affected_rows > 0


def sql_delete_wanted(wanted_id: int, user_id: int) -> bool:
    """
    删除求购（只能删除自己的）
    """
    delete_sql = "DELETE FROM wanted WHERE wanted_id = %s AND user_id = %s"
    
    with get_cursor(commit=True) as cursor:
        cursor.execute(delete_sql, (wanted_id, user_id))
        affected_rows = cursor.rowcount
    
    return affected_rows > 0
