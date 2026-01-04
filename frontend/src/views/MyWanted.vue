<template>
  <div class="my-wanted-container">
    <NavBar />
    <div class="content-wrapper">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>我的求购</span>
            <el-button type="primary" size="small" @click="$router.push('/wanted/publish')">发布求购</el-button>
          </div>
        </template>

        <el-table :data="list" v-loading="loading" style="width:100%">
          <el-table-column prop="title" label="标题" min-width="200" />
          <el-table-column label="分类" width="120">
            <template #default="{ row }"><el-tag size="small">{{ row.category }}</el-tag></template>
          </el-table-column>
          <el-table-column label="期望价" width="120">
            <template #default="{ row }">¥ {{ row.expected_price }}</template>
          </el-table-column>
          <el-table-column label="状态" width="120">
            <template #default="{ row }">
              <el-select v-model="row.status" size="small" @change="(val)=>updateStatus(row, val)">
                <el-option label="进行中" :value="0" />
                <el-option label="已完成" :value="1" />
                <el-option label="已取消" :value="2" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="goDetail(row.wanted_id)">查看</el-button>
              <el-button size="small" type="primary" link @click="goEdit(row.wanted_id)">编辑</el-button>
              <el-button size="small" type="danger" @click="remove(row.wanted_id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

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
import { ElMessage, ElMessageBox } from 'element-plus'
import NavBar from '@/components/NavBar.vue'
import { getMyWantedList, updateWantedStatus, deleteWanted } from '@/api/wanted'
import { useRouter } from 'vue-router'

const router = useRouter()
const list = ref([])
const loading = ref(false)
const pagination = reactive({ page: 1, page_size: 10, total: 0 })

const loadData = async () => {
  loading.value = true
  try {
    const res = await getMyWantedList({ page: pagination.page, page_size: pagination.page_size })
    if (res.code === 200) {
      pagination.total = res.data.total
      list.value = res.data.list || []
    }
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (p) => {
  pagination.page = p
  loadData()
}

const updateStatus = async (row, status) => {
  const res = await updateWantedStatus(row.wanted_id, status)
  if (res.code === 200) {
    ElMessage.success('状态已更新')
  } else {
    ElMessage.error(res.message || '更新失败')
    loadData()
  }
}

const remove = (id) => {
  ElMessageBox.confirm('确定删除该求购吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    const res = await deleteWanted(id)
    if (res.code === 200) {
      ElMessage.success('已删除')
      loadData()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  }).catch(() => {})
}

const goDetail = (id) => router.push(`/wanted/detail/${id}`)
const goEdit = (id) => router.push(`/wanted/edit/${id}`)

onMounted(loadData)
</script>

<style scoped>
.my-wanted-container {
  min-height: 100vh;
  background: #f0f7ff;
  padding-top: 70px;
}

.content-wrapper {
  max-width: 100%;
  margin: 0;
  padding: 24px 40px;
}

.content-wrapper :deep(.el-card) {
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 18px;
  font-weight: bold;
  color: #1976d2;
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
