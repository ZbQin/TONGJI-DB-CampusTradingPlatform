import request from '@/utils/request'

// 获取会话列表
export function getSessionList() {
  return request({
    url: '/chat/session-list',
    method: 'get'
  })
}

// 创建或获取会话
export function getOrCreateSession(data) {
  return request({
    url: '/chat/get-or-create-session',
    method: 'post',
    data
  })
}

// 获取会话消息列表
export function getMessageList(session_id) {
  return request({
    url: '/chat/message-list',
    method: 'get',
    params: { session_id }
  })
}

// 发送消息
export function sendMessage(data) {
  return request({
    url: '/chat/send-message',
    method: 'post',
    data
  })
}

// 标记消息为已读
export function markMessagesRead(session_id) {
  return request({
    url: '/chat/mark-read',
    method: 'post',
    data: { session_id }
  })
}

// 上传聊天图片
export function uploadChatImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/chat/upload-image',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除会话
export function deleteSession(session_id) {
  return request({
    url: '/chat/delete-session',
    method: 'post',
    data: { session_id }
  })
}

// 获取未读消息数
export function getUnreadCount() {
  return request({
    url: '/chat/unread-count',
    method: 'get'
  })
}

// 按 user_id 查询用户信息（昵称、头像）
export function getUserInfo(user_id) {
  return request({
    url: `/chat/user/${user_id}`,
    method: 'get'
  })
}
