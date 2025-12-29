"""评价路由。"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..sqls.review_sql import (
    create_review,
    get_review_by_id,
    get_reviews_by_reviewee,
    get_reviews_by_reviewer,
    get_user_rating_stats,
    delete_review
)
from ..sqls.auth_sql import get_user_by_id

review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    """创建评价。"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    reviewee_id = data.get('reviewee_id')
    product_id = data.get('product_id')
    rating = data.get('rating')
    content = data.get('content', '')
    
    if not reviewee_id or not rating:
        return jsonify({'code': 400, 'message': '被评价者ID和评分不能为空', 'data': None})
    
    if rating < 1 or rating > 5:
        return jsonify({'code': 400, 'message': '评分必须在1-5之间', 'data': None})
    
    if user_id == reviewee_id:
        return jsonify({'code': 400, 'message': '不能评价自己', 'data': None})
    
    # 检查被评价者是否存在
    reviewee = get_user_by_id(reviewee_id)
    if not reviewee:
        return jsonify({'code': 400, 'message': '被评价者不存在', 'data': None})
    
    review_id = create_review(user_id, reviewee_id, product_id, rating, content)
    
    return jsonify({
        'code': 200,
        'message': '评价成功',
        'data': {'review_id': review_id}
    })


@review_bp.route('/detail/<int:review_id>', methods=['GET'])
def detail(review_id):
    """获取评价详情。"""
    review = get_review_by_id(review_id)
    if not review:
        return jsonify({'code': 404, 'message': '评价不存在', 'data': None})
    
    return jsonify({'code': 200, 'message': 'success', 'data': review})


@review_bp.route('/list-received', methods=['GET'])
def list_received():
    """获取用户收到的评价列表。"""
    # 支持通过user_id参数查看指定用户的评价
    target_user_id = request.args.get('user_id', type=int)
    
    # if not target_user_id:
    #     # 如果没有传user_id，尝试从JWT获取当前用户
    #     try:
    #         from flask_jwt_extended import verify_jwt_in_request
    #         verify_jwt_in_request(optional=True)
    #         jwt_identity = get_jwt_identity()
    #         if jwt_identity:
    #             target_user_id = int(jwt_identity)
    #     except:
    #         pass
    
    if not target_user_id:
        return jsonify({'code': 400, 'message': '缺少user_id参数', 'data': None})
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = get_reviews_by_reviewee(target_user_id, page, page_size)
    return jsonify({'code': 200, 'message': 'success', 'data': result})


@review_bp.route('/list-sent', methods=['GET'])
@jwt_required()
def list_sent():
    """获取当前用户发出的评价列表。"""
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    result = get_reviews_by_reviewer(user_id, page, page_size)
    return jsonify({'code': 200, 'message': 'success', 'data': result})


@review_bp.route('/user-stats/<int:target_user_id>', methods=['GET'])
def user_stats(target_user_id):
    """获取指定用户的评分统计。"""
    stats = get_user_rating_stats(target_user_id)
    return jsonify({'code': 200, 'message': 'success', 'data': stats})


@review_bp.route('/delete/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete(review_id):
    """删除评价（仅限评价者本人）。"""
    user_id = int(get_jwt_identity())
    
    review = get_review_by_id(review_id)
    if not review:
        return jsonify({'code': 404, 'message': '评价不存在', 'data': None})
    
    if review['reviewer_id'] != user_id:
        return jsonify({'code': 403, 'message': '无权删除此评价', 'data': None})
    
    success = delete_review(review_id)
    if success:
        return jsonify({'code': 200, 'message': '删除成功', 'data': True})
    else:
        return jsonify({'code': 500, 'message': '删除失败', 'data': False})
