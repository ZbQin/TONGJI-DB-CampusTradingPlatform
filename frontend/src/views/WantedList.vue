<template>
  <div class="wanted-container">
    <NavBar />
    <div class="content-wrapper page-shell">
      <div class="hero-shell wanted-hero">
        <div>
          <div class="floating-badge">实时求购</div>
          <h2>寻找心愿，快速响应</h2>
          <p class="section-sub">发布求购或回应同学的需求，促成校园内的高效匹配</p>
        </div>
        <div class="actions">
          <el-button type="primary" @click="$router.push('/wanted/publish')">发布求购</el-button>
          <el-button class="ghost-button" @click="$router.push('/wanted/my-list')">我的求购</el-button>
        </div>
      </div>

      <el-card class="soft-card glass">
        <div class="filters">
          <el-select v-model="filters.category_id" placeholder="分类" clearable @change="reload">
            <el-option v-for="c in categories" :key="c.category_id" :label="c.name" :value="c.category_id" />
          </el-select>
          <el-select v-model="filters.status" placeholder="状态" @change="reload">
            <el-option label="进行中" :value="0" />
            <el-option label="已完成" :value="1" />
            <el-option label="已取消" :value="2" />
          </el-select>
        </div>

        <el-skeleton :rows="4" v-if="loading" animated />
        <div v-else class="list">
          <el-empty v-if="list.length === 0" description="暂无求购" />
          <el-card v-for="item in list" :key="item.wanted_id" class="wanted-card" shadow="hover" @click="goDetail(item.wanted_id)">
            <div class="title-line">
              <h3>{{ item.title }}</h3>
              <el-tag size="small">{{ item.category }}</el-tag>
            </div>
            <p class="desc">{{ item.description }}</p>
            <div class="meta">
              <div class="user">
                <el-avatar :size="24" :src="item.publisher.avatar" />
                <span class="nickname">{{ item.publisher.nickname }}</span>
              </div>
              <div class="price">期望 ¥ {{ item.expected_price }}</div>
              <div class="time">{{ item.created_at }}</div>
            </div>
          </el-card>
        </div>

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
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import NavBar from '@/components/NavBar.vue'
import { getWantedList } from '@/api/wanted'
import { getCategoryList } from '@/api/category'
import { ElMessage } from 'element-plus'

const store = useStore()
const list = ref([])
const loading = ref(false)
const categories = ref([])
const filters = reactive({ category_id: null, status: 0 })
const pagination = reactive({ page: 1, page_size: 10, total: 0 })
const router = useRouter()

const loadCategories = async () => {
  try {
    const res = await getCategoryList()
    if (res.code === 200) categories.value = res.data
  } catch (error) {
    console.error(error)
  }
}

const loadList = async () => {
  loading.value = true
  try {
    const res = await getWantedList({
      page: pagination.page,
      page_size: pagination.page_size,
      category_id: filters.category_id,
      status: filters.status
    })
    if (res.code === 200) {
      pagination.total = res.data.total
      list.value = res.data.list || []
    }
  } catch (error) {
    ElMessage.error('加载求购失败')
  } finally {
    loading.value = false
  }
}

const reload = () => {
  pagination.page = 1
  loadList()
}

const handlePageChange = (p) => {
  pagination.page = p
  loadList()
}

const goDetail = (id) => {
  router.push(`/wanted/detail/${id}`)
}

onMounted(() => {
  loadCategories()
  loadList()
})
</script>

<style scoped>
.wanted-container {
  min-height: 100vh;
  background: #f0f7ff;
  padding-top: 70px;
}

.content-wrapper {
  max-width: 100%;
  margin: 0;
  padding: 24px 40px;
}

.wanted-hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
}

.wanted-hero h2 {
  font-size: 24px;
  margin: 8px 0 4px 0;
  color: #303133;
}

.wanted-hero .section-sub {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.actions {
  display: flex;
  gap: 10px;
}

.soft-card {
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
  padding: 20px;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.wanted-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e3f2fd;
}

.wanted-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(33, 150, 243, 0.2);
  border-color: #2196f3;
}

.wanted-card :deep(.el-card__body) {
  padding: 16px;
}

.title-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}

.title-line h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.desc {
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.6;
  font-size: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  color: #909399;
  font-size: 13px;
}

.user {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nickname {
  font-weight: 500;
  color: #606266;
}

.price {
  color: #f56c6c;
  font-weight: 600;
  font-size: 16px;
}

.time {
  color: #c0c4cc;
  font-size: 12px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.pagination :deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background: #2196f3;
}
</style>
