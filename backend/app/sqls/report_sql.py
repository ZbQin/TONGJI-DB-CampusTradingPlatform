"""举报相关的 SQL 操作。"""
from typing import Optional, List, Dict
from datetime import datetime, timezone
from ..utils.db_helper import get_cursor


def create_report(reporter_id: int, reported_id: Optional[int], target_type: int, target_id: int, 
                  reason: str, description: str) -> int:
    """创建举报。"""
    now = datetime.now(timezone.utc)
    sql = """
        INSERT INTO reports (reporter_id, reported_id, target_type, target_id, reason, description, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, 0, %s)
    """
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (reporter_id, reported_id, target_type, target_id, reason, description, now))
        report_id = cursor.lastrowid
    return report_id


def get_report_by_id(report_id: int) -> Optional[Dict]:
    """根据ID查询举报。"""
    sql = """
        SELECT r.*, 
               u1.nickname as reporter_nickname, u1.avatar as reporter_avatar,
               u2.nickname as reported_nickname, u2.avatar as reported_avatar,
               a.username as handler_username
        FROM reports r
        LEFT JOIN user u1 ON r.reporter_id = u1.user_id
        LEFT JOIN user u2 ON r.reported_id = u2.user_id
        LEFT JOIN admins a ON r.handler_id = a.admin_id
        WHERE r.report_id = %s
    """
    with get_cursor() as cursor:
        cursor.execute(sql, (report_id,))
        row = cursor.fetchone()
    return dict(row) if row else None


def get_report_list(page: int = 1, page_size: int = 20, status: Optional[int] = None, 
                    target_type: Optional[int] = None) -> Dict:
    """查询举报列表（管理员）。"""
    offset = (page - 1) * page_size
    conditions = []
    params = []
    
    if status is not None:
        conditions.append("r.status = %s")
        params.append(status)
    if target_type is not None:
        conditions.append("r.target_type = %s")
        params.append(target_type)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # 查询总数
    count_sql = f"SELECT COUNT(*) as total FROM reports r WHERE {where_clause}"
    with get_cursor() as cursor:
        cursor.execute(count_sql, tuple(params))
        total = cursor.fetchone()['total']
    
    # 查询列表
    list_sql = f"""
        SELECT r.*, 
               u1.nickname as reporter_nickname, u1.avatar as reporter_avatar,
               u2.nickname as reported_nickname, u2.avatar as reported_avatar
        FROM reports r
        LEFT JOIN user u1 ON r.reporter_id = u1.user_id
        LEFT JOIN user u2 ON r.reported_id = u2.user_id
        WHERE {where_clause}
        ORDER BY r.created_at DESC
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


def get_my_reports(reporter_id: int, page: int = 1, page_size: int = 20) -> Dict:
    """查询我的举报列表。"""
    offset = (page - 1) * page_size
    
    # 查询总数
    count_sql = "SELECT COUNT(*) as total FROM reports WHERE reporter_id = %s"
    with get_cursor() as cursor:
        cursor.execute(count_sql, (reporter_id,))
        total = cursor.fetchone()['total']
    
    # 查询列表
    list_sql = """
        SELECT r.*, 
               u2.nickname as reported_nickname, u2.avatar as reported_avatar
        FROM reports r
        LEFT JOIN user u2 ON r.reported_id = u2.user_id
        WHERE r.reporter_id = %s
        ORDER BY r.created_at DESC
        LIMIT %s OFFSET %s
    """
    with get_cursor() as cursor:
        cursor.execute(list_sql, (reporter_id, page_size, offset))
        rows = cursor.fetchall()
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': [dict(row) for row in rows] if rows else []
    }


def handle_report(report_id: int, handler_id: int, status: int, handle_result: str) -> bool:
    """处理举报（管理员）。"""
    now = datetime.now(timezone.utc)
    sql = """
        UPDATE reports 
        SET status = %s, handler_id = %s, handle_result = %s, handle_time = %s
        WHERE report_id = %s
    """
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (status, handler_id, handle_result, now, report_id))
        return cursor.rowcount > 0


def delete_report(report_id: int) -> bool:
    """删除举报。"""
    sql = "DELETE FROM reports WHERE report_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (report_id,))
        return cursor.rowcount > 0
