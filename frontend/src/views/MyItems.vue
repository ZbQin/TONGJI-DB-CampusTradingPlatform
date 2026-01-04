<template>
  <div class="my-items-container">
    <NavBar />
    
    <div class="content-wrapper">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>我的发布</span>
            <el-button type="primary" size="small" @click="$router.push('/publish')">发布新商品</el-button>
          </div>
        </template>
        
        <el-table :data="myProducts" style="width: 100%" v-loading="loading">
          <el-table-column prop="image" label="图片" width="100">
            <template #default="scope">
              <img v-if="scope.row.image" :src="scope.row.image" style="width: 60px; height: 60px; object-fit: cover" />
              <div v-else style="width: 60px; height: 60px; background: #f5f7fa; display: flex; align-items: center; justify-content: center; color: #909399; font-size: 12px;">无图</div>
            </template>
          </el-table-column>
          
          <el-table-column prop="title" label="商品标题" min-width="200" />
          
          <el-table-column prop="price" label="价格" width="120">
            <template #default="scope">
              <span style="color: #f56c6c; font-weight: bold;">¥ {{ scope.row.price }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="category" label="分类" width="120">
            <template #default="scope">
              <el-tag size="small">{{ scope.row.category }}</el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'" size="small">
                {{ scope.row.status === 'active' ? '在售' : '已下架' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="create_time" label="发布时间" width="180" />
          
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDelete(scope.row)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import NavBar from '@/components/NavBar.vue'
import { getMyProductList, deleteProduct } from '@/api/product'

const router = useRouter()
const loading = ref(false)
const myProducts = ref([])

onMounted(async () => {
  fetchData()
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getMyProductList({ page: 1, page_size: 100 })
    if (res.code === 200) {
      myProducts.value = res.data.list.map(item => ({
        id: item.product_id,
        title: item.title,
        price: item.price,
        category: item.category,
        status: item.status === 0 ? 'active' : 'sold',
        create_time: item.created_at,
        image: item.images && item.images.length > 0 ? item.images[0] : ''
      }))
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  router.push(`/product/edit/${row.id}`)
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该商品吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      const res = await deleteProduct(row.id)
      if (res.code === 200) {
        ElMessage.success('删除成功')
        fetchData()
      } else {
        ElMessage.error(res.message || '删除失败')
      }
    })
    .catch(() => {})
}
</script>

<style scoped>
.my-items-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.content-wrapper {
  max-width: 1000px;
  margin: 20px auto;
  padding: 0 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>