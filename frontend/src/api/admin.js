import request from '@/utils/request'

/**
 * 管理员登录（admins表）
 */
export function adminLogin(data) {
  return request({
    url: '/admin/login',
    method: 'post',
    data
  })
}

/**
 * 封禁用户
 */
export function banUser(userId, data) {
  return request({
    url: `/admin/ban-user/${userId}`,
    method: 'post',
    data
  })
}

/**
 * 解封用户
 */
export function unbanUser(userId) {
  return request({
    url: `/admin/unban-user/${userId}`,
    method: 'post'
  })
}

/**
 * 管理员发送通知
 */
export function sendNotification(data) {
  return request({
    url: '/admin/send-notification',
    method: 'post',
    data
  })
}

/**
 * 获取举报列表（管理员）
 */
export function getReportList(params) {
  return request({
    url: '/report/list',
    method: 'get',
    params
  })
}

/**
 * 处理举报
 */
export function handleReport(reportId, data) {
  return request({
    url: `/report/handle/${reportId}`,
    method: 'post',
    data
  })
}

/**
 * 删除举报
 */
export function deleteReport(reportId) {
  return request({
    url: `/report/delete/${reportId}`,
    method: 'delete'
  })
}

