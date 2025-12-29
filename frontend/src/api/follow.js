import request from '@/utils/request'

// 关注用户
export function addFollow(user_id) {
  return request({
    url: '/follow/add',
    method: 'post',
    data: { user_id }
  })
}

// 取消关注
export function cancelFollow(user_id) {
  return request({
    url: '/follow/cancel',
    method: 'post',
    data: { user_id }
  })
}

// 获取关注列表（我关注的人）
export function getFollowing(params) {
  return request({
    url: '/follow/following',
    method: 'get',
    params
  })
}

// 获取粉丝列表（关注我的人）
export function getFollowers(params) {
  return request({
    url: '/follow/followers',
    method: 'get',
    params
  })
}

// 检查是否关注
export function checkFollowing(user_id) {
  return request({
    url: '/follow/check',
    method: 'get',
    params: { user_id }
  })
}

// 获取关注统计
export function getFollowStats(user_id) {
  return request({
    url: '/follow/stats',
    method: 'get',
    params: { user_id }
  })
}
