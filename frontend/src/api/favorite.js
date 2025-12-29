import request from '@/utils/request'

// 添加收藏
export function addFavorite(product_id) {
  return request({
    url: '/favorite/add',
    method: 'post',
    data: { product_id }
  })
}

// 取消收藏
export function cancelFavorite(product_id) {
  return request({
    url: '/favorite/cancel',
    method: 'post',
    data: { product_id }
  })
}

// 我的收藏列表
export function getMyFavoriteList(params) {
  return request({
    url: '/favorite/my-list',
    method: 'get',
    params
  })
}

// 检查是否收藏
export function checkFavorite(product_id) {
  return request({
    url: '/favorite/check',
    method: 'get',
    params: { product_id }
  })
}
