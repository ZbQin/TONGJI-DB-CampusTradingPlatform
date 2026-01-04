<template>
  <div class="chat-container">
    <NavBar />
    
    <div class="chat-main glass-shell">
      <!-- 左侧会话列表 -->
      <div class="session-list glass-card">
        <div class="session-header">
          <h3>消息</h3>
          <el-badge :value="totalUnread" :hidden="totalUnread === 0" class="unread-badge" />
        </div>
        
        <el-scrollbar class="session-scroll">
          <div 
            v-for="session in sessions" 
            :key="session.session_id"
            :class="['session-item', { active: currentSessionId === session.session_id }]"
            @click="selectSession(session.session_id)"
          >
            <el-avatar :size="50" :src="getOtherUserAvatar(session)" class="session-avatar">
              {{ getOtherUserName(session)?.charAt(0) }}
            </el-avatar>
            <div class="session-info">
              <div class="session-top">
                <span class="session-name">{{ getOtherUserName(session) }}</span>
                <span class="session-time">{{ formatTime(session.updated_at) }}</span>
              </div>
              <div class="session-bottom">
                <span class="last-message">{{ session.last_message || '暂无消息' }}</span>
                <el-badge 
                  v-if="session.unread_count > 0" 
                  :value="session.unread_count" 
                  class="unread-count"
                />
              </div>
            </div>
          </div>
          
          <el-empty v-if="sessions.length === 0" description="暂无聊天记录" />
        </el-scrollbar>
      </div>

      <!-- 右侧聊天区域 -->
      <div class="chat-area glass-card">
        <div v-if="!currentSessionId" class="no-session">
          <el-empty description="请选择一个会话开始聊天" />
        </div>
        
        <template v-else>
          <!-- 聊天头部 -->
          <div class="chat-header">
            <div class="chat-user-info">
              <el-avatar :size="40" :src="currentSession?.avatar" />
              <span class="chat-user-name">{{ currentSession?.name }}</span>
            </div>
            <el-button 
              type="danger" 
              text 
              :icon="Delete" 
              @click="handleDeleteSession"
            >
              删除会话
            </el-button>
          </div>

          <!-- 消息列表 -->
          <el-scrollbar ref="messageScrollbar" class="message-list">
            <div 
              v-for="msg in messages" 
              :key="msg.message_id"
              :class="['message-item', msg.sender_id === currentUserId ? 'message-right' : 'message-left']"
            >
              <el-avatar 
                :size="40" 
                :src="msg.sender_id === currentUserId ? userInfo.avatar : currentSession?.avatar" 
              />
              <div class="message-content">
                <div class="message-info">
                  <span class="sender-name">
                    {{ msg.sender_id === currentUserId ? '我' : currentSession?.name }}
                  </span>
                  <span class="message-time">{{ formatTime(msg.created_at) }}</span>
                </div>
                <div class="message-bubble">
                  <template v-if="msg.message_type === 0">
                    {{ msg.content }}
                  </template>
                  <template v-else>
                    <el-image 
                      :src="msg.content" 
                      :preview-src-list="[msg.content]"
                      fit="cover"
                      class="message-image"
                    />
                  </template>
                </div>
              </div>
            </div>
            
            <el-empty v-if="messages.length === 0" description="暂无消息" />
          </el-scrollbar>

          <!-- 输入区域 -->
          <div class="input-area">
            <div class="input-toolbar">
              <el-upload
                :show-file-list="false"
                :before-upload="handleImageUpload"
                accept="image/*"
              >
                <el-button :icon="Picture" circle />
              </el-upload>
            </div>
            <div class="input-box">
              <el-input
                v-model="messageInput"
                type="textarea"
                :rows="3"
                placeholder="输入消息..."
                @keydown.enter.prevent="handleSendMessage"
              />
              <el-button 
                type="primary" 
                :icon="Promotion"
                :loading="sending"
                @click="handleSendMessage"
              >
                发送
              </el-button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import NavBar from '@/components/NavBar.vue'
import { Delete, Picture, Promotion } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getSessionList,
  getMessageList,
  sendMessage,
  markMessagesRead,
  uploadChatImage,
  deleteSession,
  getUserInfo
} from '@/api/chat'

const router = useRouter()
const store = useStore()

const sessions = ref([])
const messages = ref([])
const currentSessionId = ref(null)
const messageInput = ref('')
const sending = ref(false)
const messageScrollbar = ref(null)

const userInfo = computed(() => store.state.userInfo || {})
const currentUserId = computed(() => userInfo.value.user_id || null)

const currentSession = computed(() => {
  if (!currentSessionId.value) return null
  const session = sessions.value.find(s => s.session_id === currentSessionId.value)
  if (!session) return null
  
  return {
    name: getOtherUserName(session),
    avatar: getOtherUserAvatar(session)
  }
})

const totalUnread = computed(() => {
  return sessions.value.reduce((sum, session) => sum + (session.unread_count || 0), 0)
})

// 获取对方用户名
const getOtherUserName = (session) => {
  const isCurrentUserBuyer = session.buyer_id === currentUserId.value
  const other = isCurrentUserBuyer ? session.seller : session.buyer
  if (!other) {
    return isCurrentUserBuyer ? `卖家 #${session.seller_id}` : `买家 #${session.buyer_id}`
  }
  return other.nickname || `用户 #${other.user_id}`
}

// 获取对方用户头像
const getOtherUserAvatar = (session) => {
  const isCurrentUserBuyer = session.buyer_id === currentUserId.value
  const other = isCurrentUserBuyer ? session.seller : session.buyer
  const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
  if (!other) return defaultAvatar
  return other.avatar || defaultAvatar
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return `${date.getMonth() + 1}-${date.getDate()}`
}

// 加载会话列表
const loadSessions = async () => {
  try {
    const res = await getSessionList()
    if (res.code === 200) {
      sessions.value = res.data.list || []

      // 补充会话中缺失的用户信息（buyer/seller）以便显示 nickname/avatar
      const fillPromises = sessions.value.map(async (session) => {
        // 确定对方 id
        const isCurrentUserBuyer = session.buyer_id === currentUserId.value
        const otherId = isCurrentUserBuyer ? session.seller_id : session.buyer_id

        // 如果会话里已经有 buyer/seller 对象则跳过
        if (isCurrentUserBuyer && session.seller) return
        if (!isCurrentUserBuyer && session.buyer) return

        try {
          const r = await getUserInfo(otherId)
          if (r && r.code === 200 && r.data) {
            if (isCurrentUserBuyer) {
              session.seller = r.data
            } else {
              session.buyer = r.data
            }
          }
        } catch (e) {
          // 忽略单条用户获取错误
          console.error('获取用户信息失败', otherId, e)
        }
      })

      await Promise.all(fillPromises)
    }
  } catch (error) {
    ElMessage.error('加载会话列表失败')
  }
}

// 选择会话
const selectSession = async (sessionId) => {
  currentSessionId.value = sessionId
  await loadMessages(sessionId)
  await markRead(sessionId)
}

// 加载消息列表
const loadMessages = async (sessionId) => {
  try {
    const res = await getMessageList(sessionId)
    if (res.code === 200) {
      messages.value = res.data.list || []
      await nextTick()
      scrollToBottom()
    } 
    else {
      ElMessage.error(res.data.message)
    }
  } catch (error) {
    ElMessage.error('加载消息失败')
  }
}

// 标记为已读
const markRead = async (sessionId) => {
  try {
    await markMessagesRead(sessionId)
    // 更新会话列表中的未读数
    const session = sessions.value.find(s => s.session_id === sessionId)
    if (session) {
      session.unread_count = 0
    }
  } catch (error) {
    console.error('标记已读失败', error)
  }
}

// 发送消息
const handleSendMessage = async () => {
  if (!messageInput.value.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }
  
  if (!currentSessionId.value) {
    ElMessage.warning('请先选择一个会话')
    return
  }
  
  if (!currentUserId.value) {
    ElMessage.error('用户信息未加载，请刷新页面')
    return
  }
  
  const session = sessions.value.find(s => s.session_id === currentSessionId.value)
  if (!session) return
  
  const receiverId = session.buyer_id === currentUserId.value ? session.seller_id : session.buyer_id
  
  sending.value = true
  try {
    const res = await sendMessage({
      session_id: currentSessionId.value,
      receiver_id: receiverId,
      message_type: 0,
      content: messageInput.value
    })
    
    if (res.code === 200) {
      messages.value.push(res.data)
      messageInput.value = ''
      await nextTick()
      scrollToBottom()
      
      // 更新会话列表
      session.last_message = res.data.content
      session.updated_at = res.data.created_at
      
      // 将当前会话移到最前
      sessions.value = [
        session,
        ...sessions.value.filter(s => s.session_id !== currentSessionId.value)
      ]
    } else {
      ElMessage.error(res.message || '发送失败')
    }
  } catch (error) {
    ElMessage.error('发送失败')
  } finally {
    sending.value = false
  }
}

// 上传图片
const handleImageUpload = async (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  
  if (!currentUserId.value) {
    ElMessage.error('用户信息未加载，请刷新页面')
    return false
  }
  
  try {
    const res = await uploadChatImage(file)
    if (res.code === 200) {
      const session = sessions.value.find(s => s.session_id === currentSessionId.value)
      if (!session) {
        ElMessage.error('会话不存在')
        return false
      }
      
      const receiverId = session.buyer_id === currentUserId.value ? session.seller_id : session.buyer_id
      
      const msgRes = await sendMessage({
        session_id: currentSessionId.value,
        receiver_id: receiverId,
        message_type: 1,
        content: res.data.image_url
      })
      
      if (msgRes.code === 200) {
        messages.value.push(msgRes.data)
        await nextTick()
        scrollToBottom()
      }
    } else {
      ElMessage.error(res.message || '上传失败')
    }
  } catch (error) {
    ElMessage.error('上传失败')
  }
  
  return false
}

// 删除会话
const handleDeleteSession = () => {
  ElMessageBox.confirm('确定删除此会话吗？删除后消息记录将无法恢复。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const res = await deleteSession(currentSessionId.value)
      if (res.code === 200) {
        ElMessage.success('删除成功')
        sessions.value = sessions.value.filter(s => s.session_id !== currentSessionId.value)
        currentSessionId.value = null
        messages.value = []
      } else {
        ElMessage.error(res.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 立即滚到底部
const scrollToBottom = () => {
  if (!messageScrollbar.value) return

  let wrap = null
    
  wrap = messageScrollbar.value.$el.querySelector('.el-scrollbar__wrap')
  
  if (!wrap) return

  // 立即跳到底部
  wrap.scrollTop = wrap.scrollHeight
}

onMounted(async () => {
  // 确保用户信息已加载
  if (!store.state.userInfo || !store.state.userInfo.user_id) {
    try {
      await store.dispatch('fetchUserInfo')
    } catch (error) {
      ElMessage.error('获取用户信息失败')
      router.push('/login')
      return
    }
  }
  
  loadSessions()
})
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
}

.glass-shell {
  padding: 20px;
  margin: 80px auto 20px;
  max-width: 1400px;
  width: 100%;
}

.glass-card {
  background: var(--glass);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
}

.chat-main {
  flex: 1;
  display: flex;
  gap: 20px;
  overflow: hidden;
}

/* 左侧会话列表 */
.session-list {
  width: 320px;
  display: flex;
  flex-direction: column;
}

.session-header {
  padding: 20px;
  border-bottom: 1px solid rgba(33, 150, 243, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.session-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1976d2;
}

.session-scroll {
  flex: 1;
  height: 0;
}

.session-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  border-bottom: 1px solid rgba(33, 150, 243, 0.05);
  transition: all 0.3s;
}

.session-item:hover {
  background: rgba(33, 150, 243, 0.08);
}

.session-item.active {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.15), rgba(25, 118, 210, 0.2));
  border-left: 3px solid #2196f3;
}

.session-avatar {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
  font-weight: bold;
}

.session-info {
  flex: 1;
  margin-left: 12px;
  min-width: 0;
}

.session-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.session-name {
  font-weight: 600;
  font-size: 15px;
  color: #1976d2;
}

.session-time {
  font-size: 12px;
  color: #999;
}

.session-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.last-message {
  flex: 1;
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 右侧聊天区域 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.no-session {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(33, 150, 243, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(33, 150, 243, 0.05);
}

.chat-user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-user-name {
  font-weight: 600;
  font-size: 16px;
  color: #1976d2;
}

.message-list {
  flex: 1;
  height: 0;
  padding: 20px;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  gap: 10px;
}

.message-item.message-right {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 60%;
  display: flex;
  flex-direction: column;
}

.message-right .message-content {
  align-items: flex-end;
}

.message-info {
  display: flex;
  gap: 8px;
  margin-bottom: 5px;
  font-size: 12px;
  color: #999;
}

.message-bubble {
  background: rgba(33, 150, 243, 0.08);
  padding: 10px 15px;
  border-radius: 12px;
  word-break: break-word;
  font-size: 14px;
  color: #333;
}

.message-right .message-bubble {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
}

.message-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 4px;
  cursor: pointer;
}

.input-area {
  border-top: 1px solid #e0e0e0;
  padding: 15px 20px;
}

.input-toolbar {
  margin-bottom: 10px;
}

.input-box {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-box .el-input {
  flex: 1;
}
</style>
