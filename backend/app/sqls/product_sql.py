from ..utils.db_helper import get_cursor  
from datetime import datetime, timezone
import json

def sql_publish_product(title: str, description: str, price: float, category_id: int, images: list, user_id: int) -> int:
    """
    发布商品
    """
    now = datetime.now(timezone.utc)

    # 插入商品数据
    with get_cursor(commit=True) as cursor:
        cursor.execute("""
        INSERT INTO product (user_id, title, description, price, category_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, title, description,  price, category_id, 0, now, now))

        # 获取新插入商品的ID
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        product_id = cursor.fetchone()['id']

        # 插入商品图片数据
        for index, img_url in enumerate(images):
            # 第一张图片设为封面
            is_cover = 1 if index == 0 else 0
            cursor.execute("""
            INSERT INTO product_image (product_id, image_url, is_cover, sort_order, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (product_id, img_url, is_cover, index, now, now))
    
    return product_id


def sql_set_product_cover(product_id: int, image_id: int, user_id: int) -> bool:
    """
    设置商品封面图片
    """

    # 验证图片是否属于该商品
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT pi.image_id, p.user_id 
            FROM product_image pi
            JOIN product p ON pi.product_id = p.product_id
            WHERE pi.image_id = %s AND pi.product_id = %s
        """, (image_id, product_id))
        image = cursor.fetchone()
    
    if not image:
        return False
    
    # 验证用户是否是商品发布者
    if image['user_id'] != user_id:
        return False
    
    # 取消该商品所有图片的封面状态
    with get_cursor(commit=True) as cursor:
        cursor.execute("""
            UPDATE product_image 
            SET is_cover = 0 
            WHERE product_id = %s
        """, (product_id,))
        
        # 设置新的封面
        cursor.execute("""
            UPDATE product_image 
            SET is_cover = 1 
            WHERE image_id = %s
        """, (image_id,))
    
    return True


def sql_get_product_list(page: int = 1, page_size: int = 20, category_id: int = None, 
                         keyword: str = None, min_price: float = None, max_price: float = None,
                         status: int = None, sort: str = 'latest', user_id: int = None) -> dict:
    """
    获取商品列表
    """
    # 构建查询条件
    where_conditions = ["p.status != 2"]  # 排除已下架
    params = []
    
    if user_id:
        where_conditions.append("p.user_id = %s")
        params.append(user_id)
    
    if category_id:
        where_conditions.append("p.category_id = %s")
        params.append(category_id)
    
    if keyword:
        where_conditions.append("(p.title LIKE %s OR p.description LIKE %s)")
        keyword_pattern = f"%{keyword}%"
        params.extend([keyword_pattern, keyword_pattern])
    
    if min_price is not None:
        where_conditions.append("p.price >= %s")
        params.append(min_price)
    
    if max_price is not None:
        where_conditions.append("p.price <= %s")
        params.append(max_price)
    
    if status is not None:
        where_conditions.append("p.status = %s")
        params.append(status)
    
    where_clause = " AND ".join(where_conditions)
    
    # 排序
    sort_map = {
        'latest': 'p.created_at DESC',
        'price_asc': 'p.price ASC',
        'price_desc': 'p.price DESC'
    }
    order_by = sort_map.get(sort, 'p.created_at DESC')
    
    # 查询总数
    count_sql = f"SELECT COUNT(*) as total FROM product p WHERE {where_clause}"
    with get_cursor() as cursor:
        cursor.execute(count_sql, tuple(params))
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = f"""
        SELECT p.product_id, p.title, p.description, p.price, p.category_id, c.name as category_name, p.status,
               p.view_count, p.collect_count, p.created_at,
               u.user_id as seller_id, u.nickname as seller_nickname, 
               u.avatar as seller_avatar, u.credit_score as seller_credit,
               (SELECT image_url FROM product_image WHERE product_id = p.product_id AND is_cover = 1 LIMIT 1) as cover_image
        FROM product p
        LEFT JOIN user u ON p.user_id = u.user_id
        LEFT JOIN category c ON p.category_id = c.category_id
        WHERE {where_clause}
        ORDER BY {order_by}
        LIMIT %s OFFSET %s
    """
    params.extend([page_size, offset])
    with get_cursor() as cursor:
        cursor.execute(list_sql, tuple(params))
        products = cursor.fetchall()
    
    # 格式化结果
    product_list = []
    for p in products or []:
        product_list.append({
            'product_id': p['product_id'],
            'title': p['title'],
            'description': p['description'],
            'price': float(p['price']),
            'category_id': p['category_id'],
            'category': p['category_name'],
            'images': [p['cover_image']] if p['cover_image'] else [],
            'status': p['status'],
            'view_count': p['view_count'],
            'collect_count': p['collect_count'],
            'seller': {
                'user_id': p['seller_id'],
                'nickname': p['seller_nickname'],
                'avatar': p['seller_avatar'],
                'credit_score': p['seller_credit']
            },
            'created_at': p['created_at'].strftime('%Y-%m-%d %H:%M:%S') if p['created_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': product_list
    }


def sql_get_product_detail(product_id: int) -> dict:
    """
    获取商品详情
    """
    # 查询商品基本信息
    sql = """
        SELECT p.product_id, p.user_id, p.title, p.description, p.price, p.category_id, c.name as category_name, 
               p.status, p.view_count, p.collect_count, p.created_at, p.updated_at,
               u.nickname as seller_nickname, u.avatar as seller_avatar, 
               u.credit_score as seller_credit, u.campus, u.dormitory
        FROM product p
        LEFT JOIN user u ON p.user_id = u.user_id
        LEFT JOIN category c ON p.category_id = c.category_id
        WHERE p.product_id = %s
    """
    with get_cursor() as cursor:
        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()
    
    if not product:
        return None
    
    # 查询商品图片
    images_sql = """
        SELECT image_id, image_url, is_cover, sort_order
        FROM product_image
        WHERE product_id = %s
        ORDER BY is_cover DESC, sort_order ASC
    """
    with get_cursor() as cursor:
        cursor.execute(images_sql, (product_id,))
        images = cursor.fetchall()
    
    # 增加浏览次数
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE product SET view_count = view_count + 1 WHERE product_id = %s",
            (product_id,)
        )
    
    return {
        'product_id': product['product_id'],
        'user_id': product['user_id'],
        'title': product['title'],
        'description': product['description'],
        'price': float(product['price']),
        'category_id': product['category_id'],
        'category': product['category_name'],
        'status': product['status'],
        'view_count': product['view_count'] + 1,
        'collect_count': product['collect_count'],
        'images': [{'image_id': img['image_id'], 'image_url': img['image_url'], 'is_cover': img['is_cover']} 
                   for img in (images or [])],
        'seller': {
            'user_id': product['user_id'],
            'nickname': product['seller_nickname'],
            'avatar': product['seller_avatar'],
            'credit_score': product['seller_credit'],
            'campus': product['campus'],
            'dormitory': product['dormitory']
        },
        'created_at': product['created_at'].strftime('%Y-%m-%d %H:%M:%S') if product['created_at'] else None,
        'updated_at': product['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if product['updated_at'] else None
    }


def sql_get_my_product_list(user_id: int, page: int = 1, page_size: int = 20, status: int = None) -> dict:
    """
    获取我的商品列表
    """
    where_conditions = ["p.user_id = %s"]
    params = [user_id]
    
    if status is not None:
        where_conditions.append("p.status = %s")
        params.append(status)
    
    where_clause = " AND ".join(where_conditions)
    
    # 查询总数
    count_sql = f"SELECT COUNT(*) as total FROM product p WHERE {where_clause}"
    with get_cursor() as cursor:
        cursor.execute(count_sql, tuple(params))
        total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # 分页查询
    offset = (page - 1) * page_size
    list_sql = f"""
        SELECT p.product_id, p.title, p.price, p.category_id, c.name as category_name, p.status,
               p.view_count, p.collect_count, p.created_at, p.updated_at,
               (SELECT image_url FROM product_image WHERE product_id = p.product_id AND is_cover = 1 LIMIT 1) as cover_image
        FROM product p
        LEFT JOIN category c ON p.category_id = c.category_id
        WHERE {where_clause}
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s
    """
    params.extend([page_size, offset])
    with get_cursor() as cursor:
        cursor.execute(list_sql, tuple(params))
        products = cursor.fetchall()
    
    # 格式化结果
    product_list = []
    for p in products or []:
        product_list.append({
            'product_id': p['product_id'],
            'title': p['title'],
            'price': float(p['price']),
            'category_id': p['category_id'],
            'category': p['category_name'],
            'images': [p['cover_image']] if p['cover_image'] else [],
            'status': p['status'],
            'view_count': p['view_count'],
            'collect_count': p['collect_count'],
            'created_at': p['created_at'].strftime('%Y-%m-%d %H:%M:%S') if p['created_at'] else None,
            'updated_at': p['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if p['updated_at'] else None
        })
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'list': product_list
    }


def sql_update_product(product_id: int, user_id: int, **kwargs) -> bool:
    """
    修改商品信息
    """
    # 验证商品归属
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM product WHERE product_id = %s",
            (product_id,)
        )
        product = cursor.fetchone()
    
    if not product or product['user_id'] != user_id:
        return False
    
    # 允许更新的字段
    allowed_fields = ['title', 'description', 'price', 'category_id']
    updates = []
    params = []
    
    # 处理category字段名的兼容性
    if 'category' in kwargs:
        kwargs['category_id'] = kwargs.pop('category')
    
    for field in allowed_fields:
        if field in kwargs and kwargs[field] is not None:
            updates.append(f"{field} = %s")
            params.append(kwargs[field])
    
    if not updates:
        return True
    
    updates.append("updated_at = %s")
    params.append(datetime.now(timezone.utc))
    params.append(product_id)
    
    sql = f"UPDATE product SET {', '.join(updates)} WHERE product_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, tuple(params))
    return True


def sql_update_product_status(product_id: int, user_id: int, status: int) -> bool:
    """
    修改商品状态
    """
    # 验证商品归属
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM product WHERE product_id = %s",
            (product_id,)
        )
        product = cursor.fetchone()
    
    if not product or product['user_id'] != user_id:
        return False
    
    sql = "UPDATE product SET status = %s, updated_at = %s WHERE product_id = %s"
    with get_cursor(commit=True) as cursor:
        cursor.execute(sql, (status, datetime.now(timezone.utc), product_id))
    return True


def sql_delete_product(product_id: int, user_id: int) -> bool:
    """
    删除商品
    """
    # 验证商品归属
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM product WHERE product_id = %s",
            (product_id,)
        )
        product = cursor.fetchone()
    
    if not product or product['user_id'] != user_id:
        return False
    
    # 删除商品图片和商品
    with get_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM product_image WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
    return True