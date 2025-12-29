<template>
  <div class="wanted-detail">
    <NavBar />
    <div class="content-wrapper" v-loading="loading">
      <el-card v-if="detail">
        <template #header>
          <div class="card-header">
            <div class="title-box">
              <h2>{{ detail.title }}</h2>
              <el-tag size="small">{{ detail.category }}</el-tag>
              <el-tag :type="statusType(detail.status)" size="small">{{ statusText(detail.status) }}</el-tag>
            </div>
            <div class="actions">
              <el-button type="primary" plain @click="goChat">联系Ta</el-button>
            </div>
          </div>
        </template>

        <div class="meta">
          <div class="meta-item publisher-card" @click="goToUserProfile">
            <el-avatar :size="40" class="publisher-avatar">
              {{ detail.publisher.nickname?.charAt(0) }}
            </el-avatar>
            <div class="publisher-info">
              <span class="label">发布人：</span>
              <span class="value publisher-name">{{ detail.publisher.nickname }}</span>
              <el-icon class="arrow-icon"><ArrowRight /></el-icon>
            </div>
          </div>
          <div>期望价：¥ {{ detail.expected_price }}</div>
          <div>发布时间：{{ detail.created_at }}</div>
          <div>更新时间：{{ detail.updated_at }}</div>
        </div>

        <div class="section">
          <h4>求购详情</h4>
          <p>{{ detail.description }}</p>
        </div>
      </el-card>
      <el-empty v-else description="未找到该求购" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowRight } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import { getWantedDetail } from '@/api/wanted'
import { getOrCreateSession } from '@/api/chat'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const detail = ref(null)
const loading = ref(false)

const statusText = (s) => {
  if (s === 1) return '已完成'
  if (s === 2) return '已取消'
  return '进行中'
}
const statusType = (s) => {
  if (s === 1) return 'success'
  if (s === 2) return 'info'
  return 'warning'
}

const loadDetail = async () => {
  loading.value = true
  try {
    const res = await getWantedDetail(route.params.id)
    if (res.code === 200) {
      detail.value = res.data
    }
  } catch (error) {
    ElMessage.error('加载详情失败')
  } finally {
    loading.value = false
  }
}
const goChat = async () => {
  if (!detail.value) return
  try {
    const res = await getOrCreateSession({ seller_id: detail.value.publisher.user_id })
    if (res.code === 200) {
      ElMessage.success('已创建会话')
      router.push('/chat')
    }
  } catch (error) {
    ElMessage.error('创建会话失败')
  }
}

const goToUserProfile = () => {
  if (detail.value?.publisher?.user_id) {
    router.push(`/user/${detail.value.publisher.user_id}`)
  }
}

onMounted(loadDetail)
onMounted(loadDetail)
</script>

<style scoped>
.wanted-detail {
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
  justify-content: space-between;
  align-items: center;
}
.title-box {
  display: flex;
  gap: 10px;
  align-items: center;
}
.meta {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 8px;
  margin-bottom: 16px;
  color: #606266;
}

.meta-item {
  grid-column: 1 / -1;
}

.publisher-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.05), rgba(25, 118, 210, 0.08));
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(33, 150, 243, 0.1);
}

.publisher-card:hover {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(25, 118, 210, 0.15));
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
}

.publisher-avatar {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
  font-weight: bold;
}

.publisher-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.publisher-info .label {
  color: #909399;
}

.publisher-name {
  color: #2196f3;
  font-weight: bold;
}

.arrow-icon {
  color: #2196f3;
  margin-left: auto;
}

.section {
  margin-top: 16px;
}
.section h4 {
  margin-bottom: 8px;
}
.section p {
  line-height: 1.6;
  color: #303133;
}
</style>
