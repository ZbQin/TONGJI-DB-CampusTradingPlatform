"""商品分类相关的 SQL 操作"""
from typing import List, Dict, Optional
from ..utils.db_helper import get_cursor


def sql_get_category_list(status: int = None) -> List[Dict]:
    """
    获取分类列表
    :param status: 分类状态，None表示全部，1表示启用，0表示禁用
    :return: 分类列表
    """
    sql = "SELECT category_id, name, sort_order, status FROM category"
    params = []
    
    if status is not None:
        sql += " WHERE status = %s"
        params.append(status)
    
    sql += " ORDER BY sort_order ASC, category_id ASC"
    
    with get_cursor() as cursor:
        cursor.execute(sql, tuple(params) if params else None)
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows] if rows else []


def sql_get_category_by_id(category_id: int) -> Optional[Dict]:
    """
    根据ID获取分类
    :param category_id: 分类ID
    :return: 分类信息
    """
    sql = "SELECT category_id, name, sort_order, status FROM category WHERE category_id = %s"
    
    with get_cursor() as cursor:
        cursor.execute(sql, (category_id,))
        row = cursor.fetchone()
    
    return dict(row) if row else None


def sql_get_category_by_name(name: str) -> Optional[Dict]:
    """
    根据名称获取分类
    :param name: 分类名称
    :return: 分类信息
    """
    sql = "SELECT category_id, name, sort_order, status FROM category WHERE name = %s"
    
    with get_cursor() as cursor:
        cursor.execute(sql, (name,))
        row = cursor.fetchone()
    
    return dict(row) if row else None
