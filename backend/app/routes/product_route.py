from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import jwt
from ..sqls.product_sql import (
    sql_publish_product,
    sql_get_product_list,
    sql_get_product_detail,
    sql_get_my_product_list,
    sql_update_product,
    sql_update_product_status,
    sql_delete_product,
    sql_set_product_cover
)
from ..utils.helpers import allowed_file, save_upload_file

product_bp = Blueprint('product', __name__, url_prefix='/product') 

@product_bp.route('/publish', methods=['POST'])
@jwt_required()
def publish_product():
    """
    发布商品
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据为空',
                'data': None
            })
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': f'数据解析失败: {str(e)}',
            'data': None
        })
    
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')
    images = data.get('images', [])
    
    if not title or not description or not price or not category_id:
        return jsonify({
            'code': 400,
            'message': '缺少必要的商品信息',
            'data': None
        })
    
    user_id = int(get_jwt_identity())
    
    try:
        product_id = sql_publish_product(title, description, float(price), int(category_id), images, user_id)
        
        # 获取创建时间
        from datetime import datetime, timezone
        created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'code': 200,
            'message': '发布成功',
            'data': {
                'product_id': product_id,
                'created_at': created_at
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'发布失败: {str(e)}',
            'data': None
        })


@product_bp.route('/list', methods=['GET'])
def product_list():
    """
    商品列表
    """
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    category_id = request.args.get('category_id')
    keyword = request.args.get('keyword')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    status = request.args.get('status')
    sort = request.args.get('sort', 'latest')
    user_id = request.args.get('user_id')
    
    # 类型转换
    if category_id:
        category_id = int(category_id)
    if min_price:
        min_price = float(min_price)
    if max_price:
        max_price = float(max_price)
    if status:
        status = int(status)
    if user_id:
        user_id = int(user_id)
    
    try:
        result = sql_get_product_list(page, page_size, category_id, keyword, 
                                      min_price, max_price, status, sort, user_id)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}',
            'data': None
        })

    
@product_bp.route('/detail', methods=['GET'])
def product_detail():
    """
    商品详情
    """
    product_id = request.args.get('product_id')
    
    if not product_id:
        return jsonify({
            'code': 400,
            'message': '缺少商品ID',
            'data': None
        })
    
    try:
        detail = sql_get_product_detail(int(product_id))
        
        if not detail:
            return jsonify({
                'code': 404,
                'message': '商品不存在',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': detail
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}',
            'data': None
        })


@product_bp.route('/my-list', methods=['GET'])
@jwt_required()
def my_product_list():
    """
    我的商品列表
    """
    user_id = int(get_jwt_identity())
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    status = request.args.get('status')
    
    if status:
        status = int(status)
    
    try:
        result = sql_get_my_product_list(user_id, page, page_size, status)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'查询失败: {str(e)}',
            'data': None
        })


@product_bp.route('/update', methods=['POST'])
@jwt_required()
def update_product():
    """
    修改商品信息
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({
            'code': 400,
            'message': '缺少商品ID',
            'data': None
        })
    
    update_fields = {}
    if 'title' in data:
        update_fields['title'] = data['title']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'price' in data:
        update_fields['price'] = float(data['price'])
    if 'category' in data:
        update_fields['category'] = data['category']
    
    try:
        success = sql_update_product(int(product_id), user_id, **update_fields)
        
        if not success:
            return jsonify({
                'code': 403,
                'message': '无权限操作',
                'data': None
            })
        
        from datetime import datetime, timezone
        updated_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': {
                'product_id': product_id,
                'updated_at': updated_at
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}',
            'data': None
        })


@product_bp.route('/update-status', methods=['POST'])
@jwt_required()
def update_product_status():
    """
    修改商品状态
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    status = data.get('status')
    
    if not product_id or status is None:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数',
            'data': None
        })
    
    try:
        success = sql_update_product_status(int(product_id), user_id, int(status))
        
        if not success:
            return jsonify({
                'code': 403,
                'message': '无权限操作',
                'data': None
            })
        
        from datetime import datetime, timezone
        updated_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'code': 200,
            'message': '状态更新成功',
            'data': {
                'product_id': product_id,
                'status': status,
                'updated_at': updated_at
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}',
            'data': None
        })


@product_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_product():
    """
    删除商品
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({
            'code': 400,
            'message': '缺少商品ID',
            'data': None
        })
    
    try:
        success = sql_delete_product(int(product_id), user_id)
        
        if not success:
            return jsonify({
                'code': 403,
                'message': '无权限操作',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '删除成功',
            'data': True
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除失败: {str(e)}',
            'data': None
        })


@product_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_product_image():
    """
    上传商品图片
    """
    if 'file' not in request.files:
        return jsonify({
            'code': 400,
            'message': '未找到文件',
            'data': None
        })
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'code': 400,
            'message': '文件名为空',
            'data': None
        })
    
    if not allowed_file(file.filename):
        return jsonify({
            'code': 400,
            'message': '文件格式不支持',
            'data': None
        })
    
    try:
        filename = save_upload_file(file, 'product')
        image_url = f'/static/uploads/product/{filename}'
        
        return jsonify({
            'code': 200,
            'message': '上传成功',
            'data': {
                'image_url': image_url
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'上传失败: {str(e)}',
            'data': None
        })


@product_bp.route('/set-cover', methods=['POST'])
@jwt_required()
def set_cover():
    """
    设置商品封面图片
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    image_id = data.get('image_id')
    
    if not product_id or not image_id:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数',
            'data': None
        })
    
    try:
        success = sql_set_product_cover(int(product_id), int(image_id), user_id)
        
        if not success:
            return jsonify({
                'code': 403,
                'message': '无权限操作或图片不存在',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '封面设置成功',
            'data': {
                'image_id': image_id
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'设置失败: {str(e)}',
            'data': None
        })

