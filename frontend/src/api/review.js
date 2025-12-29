import request from '@/utils/request'

/**
 * 创建评价
 */
export function createReview(data) {
  return request({
    url: '/review/create',
    method: 'post',
    data
  })
}

/**
 * 获取评价详情
 */
export function getReviewById(reviewId) {
  return request({
    url: `/review/detail/${reviewId}`,
    method: 'get'
  })
}

/**
 * 获取用户收到的评价
 */
export function getReviewsByReviewee(userId) {
  return request({
    url: `/review/list-received`,
    method: 'get',
    params: { user_id: userId }
  })
}

/**
 * 获取用户发出的评价
 */
export function getReviewsByReviewer(userId) {
  return request({
    url: `/review/list-sent`,
    method: 'get',
    params: { user_id: userId }
  })
}

/**
 * 获取用户评分统计
 */
export function getUserRatingStats(userId) {
  return request({
    url: `/review/user-stats/${userId}`,
    method: 'get'
  })
}

/**
 * 删除评价
 */
export function deleteReview(reviewId) {
  return request({
    url: `/review/delete/${reviewId}`,
    method: 'delete'
  })
}
