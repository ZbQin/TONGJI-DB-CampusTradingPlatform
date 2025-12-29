import request from '@/utils/request'

// 发布求购
export function publishWanted(data) {
  return request({
    url: '/wanted/publish',
    method: 'post',
    data
  })
}

// 获取求购列表
export function getWantedList(params) {
  return request({
    url: '/wanted/list',
    method: 'get',
    params
  })
}

// 获取求购详情
export function getWantedDetail(wanted_id) {
  return request({
    url: '/wanted/detail',
    method: 'get',
    params: { wanted_id }
  })
}

// 获取我的求购
export function getMyWantedList(params) {
  return request({
    url: '/wanted/my-list',
    method: 'get',
    params
  })
}

// 更新求购状态
export function updateWantedStatus(wanted_id, status) {
  return request({
    url: '/wanted/update-status',
    method: 'post',
    data: { wanted_id, status }
  })
}

// 删除求购
export function deleteWanted(wanted_id) {
  return request({
    url: '/wanted/delete',
    method: 'post',
    data: { wanted_id }
  })
}
