<template>
  <div class="follows-container">
    <NavBar />
    <div class="content-wrapper">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>我的关注 / 粉丝</span>
            <div class="stats">
              <span>关注 {{ stats.following_count }}</span>
              <span>粉丝 {{ stats.followers_count }}</span>
            </div>
          </div>
        </template>

        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="我关注的" name="following">
            <UserList
              :list="list"
              :loading="loading"
              :action-text="'取消关注'"
              @action="handleUnfollow"
            />
          </el-tab-pane>
          <el-tab-pane label="关注我的" name="followers">
            <UserList
              :list="list"
              :loading="loading"
              :action-text="'回关'"
              @action="handleFollowBack"
              :show-action="(item) => !item.is_following"
            />
          </el-tab-pane>
        </el-tabs>

        <div class="pagination">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="pagination.total"
            :page-size="pagination.page_size"
            :current-page="pagination.page"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { getFollowing, getFollowers, addFollow, cancelFollow, getFollowStats, checkFollowing } from '@/api/follow'
import { ElMessage } from 'element-plus'
import UserList from './components/UserList.vue'

const activeTab = ref('following')
const list = ref([])
const loading = ref(false)
const stats = reactive({ following_count: 0, followers_count: 0 })
const pagination = reactive({ page: 1, page_size: 10, total: 0 })

const loadStats = async () => {
  try {
    const res = await getFollowStats()
    if (res.code === 200) {
      stats.following_count = res.data.following_count
      stats.followers_count = res.data.followers_count
    }
  } catch (error) {
    console.error(error)
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

onMounted(() => {
  loadStats()
  loadList()
})
</script>

<style scoped>
.follows-container {
  min-height: 100vh;
  background: #f5f7fa;
}
.content-wrapper {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.stats {
  display: flex;
  gap: 12px;
  color: #606266;
}
.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}
</style>
