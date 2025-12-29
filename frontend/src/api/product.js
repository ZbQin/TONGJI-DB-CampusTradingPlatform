import request from '@/utils/request'

// 发布商品
export function publishProduct(data) {
  return request({
    url: '/product/publish',
    method: 'post',
    data
  })
}

// 获取商品列表
export function getProductList(params) {
  return request({
    url: '/product/list',
    method: 'get',
    params
  })
}

// 获取商品列表(别名)
export function getProducts(params) {
  return getProductList(params)
}

// 获取用户发布的商品
export function getUserProducts(userId) {
  return request({
    url: '/product/list',
    method: 'get',
    params: { user_id: userId, pageSize: 100 }
  })
}

// 获取商品详情
export function getProductDetail(product_id) {
  return request({
    url: '/product/detail',
    method: 'get',
    params: { product_id }
  })
}

// 获取我的商品列表
export function getMyProductList(params) {
  return request({
    url: '/product/my-list',
    method: 'get',
    params
  })
}

// 修改商品信息
export function updateProduct(data) {
  return request({
    url: '/product/update',
    method: 'post',
    data
  })
}

// 修改商品状态
export function updateProductStatus(data) {
  return request({
    url: '/product/update-status',
    method: 'post',
    data
  })
}

// 删除商品
export function deleteProduct(product_id) {
  return request({
    url: '/product/delete',
    method: 'post',
    data: { product_id }
  })
}

// 上传商品图片
export function uploadProductImage(formData) {
  return request({
    url: '/product/upload-image',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 设置商品封面
export function setProductCover(data) {
  return request({
    url: '/product/set-cover',
    method: 'post',
    data
  })
}
