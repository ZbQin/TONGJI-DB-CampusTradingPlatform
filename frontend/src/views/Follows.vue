<template>
  <div class="follows-container">
    <NavBar />
    
    <div class="content-wrapper">
      <!-- 页面头部 -->
      <div class="page-header glass-card">
        <div class="header-content">
          <div class="header-left">
            <div class="floating-badge">社交管理</div>
            <h2 class="page-title">我的关注 & 粉丝</h2>
            <div class="stats-display">
              <div class="stat-item">
                <div class="stat-number">{{ stats.following_count }}</div>
                <div class="stat-label">关注</div>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <div class="stat-number">{{ stats.followers_count }}</div>
                <div class="stat-label">粉丝</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 标签页 -->
      <div class="tabs-container glass-card">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="custom-tabs">
          <el-tab-pane name="following">
            <template #label>
              <span class="tab-label">
                <el-icon><UserFilled /></el-icon>
                我关注的
              </span>
            </template>
            
            <div v-loading="loading" class="user-list-container">
              <div v-if="list.length === 0" class="empty-state">
                <el-empty description="暂无关注" />
              </div>
              <div v-else class="users-grid">
                <div v-for="item in list" :key="item.user_id" class="user-card glass-card-mini">
                  <div class="user-avatar-section">
                    <el-avatar :size="70" :src="item.avatar" class="user-avatar">
                      {{ item.nickname?.charAt(0) }}
                    </el-avatar>
                  </div>
                  <div class="user-info-section">
                    <h3 class="user-nickname">{{ item.nickname }}</h3>
                    <p class="user-phone" v-if="item.phone">{{ item.phone }}</p>
                    <p class="user-time">{{ formatTime(item.created_at) }}</p>
                  </div>
                  <div class="user-action-section">
                    <el-button
                      type="danger"
                      plain
                      size="default"
                      @click="handleUnfollow(item.user_id)"
                      class="action-btn"
                    >
                      <el-icon><Close /></el-icon>
                      取消关注
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane name="followers">
            <template #label>
              <span class="tab-label">
                <el-icon><Star /></el-icon>
                关注我的
              </span>
            </template>
            
            <div v-loading="loading" class="user-list-container">
              <div v-if="list.length === 0" class="empty-state">
                <el-empty description="暂无粉丝" />
              </div>
              <div v-else class="users-grid">
                <div v-for="item in list" :key="item.user_id" class="user-card glass-card-mini">
                  <div class="user-avatar-section">
                    <el-avatar :size="70" :src="item.avatar" class="user-avatar">
                      {{ item.nickname?.charAt(0) }}
                    </el-avatar>
                  </div>
                  <div class="user-info-section">
                    <h3 class="user-nickname">{{ item.nickname }}</h3>
                    <p class="user-phone" v-if="item.phone">{{ item.phone }}</p>
                    <p class="user-time">{{ formatTime(item.created_at) }}</p>
                  </div>
                  <div class="user-action-section">
                    <el-button
                      v-if="!item.is_following"
                      type="primary"
                      size="default"
                      @click="handleFollowBack(item.user_id)"
                      class="action-btn"
                    >
                      <el-icon><Plus /></el-icon>
                      回关
                    </el-button>
                    <el-tag v-else type="success" size="large">已关注</el-tag>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>

        <div class="pagination" v-if="pagination.total > pagination.page_size">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="pagination.total"
            :page-size="pagination.page_size"
            :current-page="pagination.page"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { UserFilled, Star, Plus, Close } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import { getFollowing, getFollowers, addFollow, cancelFollow, getFollowStats, checkFollowing } from '@/api/follow'
import { ElMessage } from 'element-plus'

const activeTab = ref('following')
const list = ref([])
const loading = ref(false)
const stats = reactive({ following_count: 0, followers_count: 0 })
const pagination = reactive({ page: 1, page_size: 12, total: 0 })

const loadStats = async () => {
  try {
    // getFollowStats不需要参数，后端会从JWT获取当前用户
    const res = await getFollowStats()
    if (res.code === 200) {
      stats.following_count = res.data.following_count || 0
      stats.followers_count = res.data.followers_count || 0
    }
  } catch (error) {
    console.error('加载统计失败:', error)
    stats.following_count = 0
    stats.followers_count = 0
  }
}

const loadList = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, page_size: pagination.page_size }
    const api = activeTab.value === 'following' ? getFollowing : getFollowers
    const res = await api(params)
    if (res.code === 200) {
      pagination.total = res.data.total
      list.value = (res.data.list || []).map(item => ({
        follow_id: item.follow_id,
        user_id: item.user_id,
        nickname: item.nickname,
        avatar: item.avatar,
        phone: item.phone,
        created_at: item.created_at,
        is_following: activeTab.value === 'following'
      }))
      // 如果是粉丝列表，补充是否已回关
      if (activeTab.value === 'followers') {
        for (const it of list.value) {
          const check = await checkFollowing(it.user_id)
          if (check.code === 200) {
            it.is_following = check.data.is_following
          }
        }
      }
    }
  } catch (error) {
    ElMessage.error('加载列表失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (p) => {
  pagination.page = p
  loadList()
}

const handleTabChange = () => {
  pagination.page = 1
  loadList()
}

const handleUnfollow = async (user_id) => {
  const res = await cancelFollow(user_id)
  if (res.code === 200) {
    ElMessage.success('已取消关注')
    loadList()
    loadStats()
  } else {
    ElMessage.error(res.message || '操作失败')
  }
}

const handleFollowBack = async (user_id) => {
  const res = await addFollow(user_id)
  if (res.code === 200) {
    ElMessage.success('已关注')
    loadList()
    loadStats()
  } else {
    ElMessage.error(res.message || '操作失败')
  }
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr + (timeStr.includes('Z') ? '' : ' UTC'))
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  if (diff < 2592000) return `${Math.floor(diff / 86400)}天前`
  return timeStr.split(' ')[0]
}

onMounted(() => {
  loadStats()
  loadList()
})
</script>

<style scoped>
.follows-container {
  min-height: 100vh;
  background: #f0f7ff;
  padding-top: 70px;
}

.content-wrapper {
  max-width: 100%;
  margin: 0;
  padding: 24px 40px;
}

.glass-card {
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
}

.glass-card-mini {
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
  transition: all 0.3s ease;
}

.glass-card-mini:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(33, 150, 243, 0.2);
  border-color: #2196f3;
}

.page-header {
  padding: 32px;
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 32px;
  font-weight: bold;
  color: #1976d2;
  margin: 8px 0 16px 0;
}

.stats-display {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #1976d2;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, transparent, #e4e7ed, transparent);
}

.tabs-container {
  padding: 24px;
}

.custom-tabs {
  margin-bottom: 20px;
}

.custom-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.custom-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.custom-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #667eea, #764ba2);
  height: 3px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 500;
}

.user-list-container {
  min-height: 400px;
}

.empty-state {
  padding: 60px 20px;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.user-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.user-avatar-section {
  position: relative;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-size: 28px;
  font-weight: bold;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.user-info-section {
  text-align: center;
  flex: 1;
  width: 100%;
}

.user-nickname {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-phone {
  font-size: 14px;
  color: #909399;
  margin: 0 0 4px 0;
}

.user-time {
  font-size: 12px;
  color: #c0c4cc;
  margin: 0;
}

.user-action-section {
  width: 100%;
}

.action-btn {
  width: 100%;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.pagination :deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background: linear-gradient(135deg, #667eea, #764ba2);
}
</style>
