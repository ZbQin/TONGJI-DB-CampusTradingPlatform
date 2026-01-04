"""数据库连接助手，使用 pymysql。

提供连接池和原始 SQL 查询执行的辅助方法。
"""
import pymysql
from pymysql.cursors import DictCursor
from flask import current_app, g
from contextlib import contextmanager


def get_db_config():
    """从 Flask 应用配置中获取数据库配置。"""
    return {
        'host': current_app.config.get('DB_HOST', '127.0.0.1'),
        'port': current_app.config.get('DB_PORT', 3306),
        'user': current_app.config.get('DB_USER', 'root'),
        'password': current_app.config.get('DB_PASSWORD', ''),
        'database': current_app.config.get('DB_NAME', 'campus_trading'),
        'charset': 'utf8mb4',
        'cursorclass': DictCursor,
        'autocommit': False
    }


def get_db():
    """从 Flask g 上下文获取数据库连接，或创建新连接。"""
    if 'db_conn' not in g:
        g.db_conn = pymysql.connect(**get_db_config())
    return g.db_conn


def close_db(e=None):
    """关闭数据库连接（如果存在）。"""
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()


@contextmanager
def get_cursor(commit=False):
    conn = get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def init_db_helper(app):
    """注册应用上下文销毁时的处理函数，用于关闭数据库连接。"""
    app.teardown_appcontext(close_db)