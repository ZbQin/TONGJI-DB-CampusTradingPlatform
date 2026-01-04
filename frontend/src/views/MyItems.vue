<template>
  <div class="my-items-container">
    <NavBar />
    
    <div class="content-wrapper">
      <div class="page-header glass-card">
        <div class="header-content">
          <div class="header-left">
            <div class="floating-badge">商品管理</div>
            <h2 class="page-title">我的发布</h2>
            <p class="page-subtitle">共 {{ myProducts.length }} 件商品</p>
          </div>
          <el-button type="primary" size="large" @click="$router.push('/publish')">
            <el-icon><Plus /></el-icon>
            发布新商品
          </el-button>
        </div>
      </div>

      <div v-loading="loading" class="products-container">
        <div v-if="myProducts.length === 0" class="empty-state">
          <el-empty description="暂无发布商品">
            <el-button type="primary" @click="$router.push('/publish')">立即发布</el-button>
          </el-empty>
        </div>
        
        <div v-else class="products-grid">
          <div v-for="item in myProducts" :key="item.id" class="product-card glass-card">
            <div class="product-image" @click="handleEdit(item)">
              <img v-if="item.image" :src="item.image" alt="商品图片" />
              <div v-else class="no-image">暂无图片</div>
              <div class="price-badge">¥{{ item.price }}</div>
              <el-tag :type="item.status === 'active' ? 'success' : 'info'" class="status-badge" size="small">
                {{ item.status === 'active' ? '在售' : '已下架' }}
              </el-tag>
            </div>
            
            <div class="product-info">
              <h3 class="product-title" @click="handleEdit(item)">{{ item.title }}</h3>
              <div class="product-meta">
                <el-tag size="small" type="info">{{ item.category }}</el-tag>
                <span class="create-time">{{ item.create_time }}</span>
              </div>
              
              <div class="product-actions">
                <el-button size="small" type="primary" @click="handleEdit(item)">
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(item)">
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
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
  margin: 8px 0;
}

.page-subtitle {
  color: #909399;
  font-size: 14px;
  margin: 0;
}

.products-container {
  min-height: 400px;
}

.empty-state {
  padding: 60px 20px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.product-card {
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(33, 150, 243, 0.2);
}

.product-image {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 14px;
}

.price-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.status-badge {
  position: absolute;
  top: 12px;
  left: 12px;
}

.product-info {
  padding: 20px;
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

.product-title:hover {
  color: #667eea;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.create-time {
  font-size: 12px;
  color: #909399;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.product-actions .el-button {
  flex: 1;
}
</style>