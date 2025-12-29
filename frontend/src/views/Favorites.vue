<template>
  <div class="favorites-container">
    <NavBar />
    
    <div class="hero-section">
      <h1>我的收藏</h1>
      <p>你收藏的所有心仪商品</p>
    </div>
    
    <div class="content-wrapper">
      <div class="products-grid" v-loading="loading">
        <div 
          class="product-card glass-card" 
          v-for="item in favorites" 
          :key="item.favorite_id"
          @click="goDetail(item.product_id)"
        >
          <div class="product-image">
            <img v-if="item.cover" :src="item.cover" :alt="item.title" />
            <div v-else class="no-image">暂无图片</div>
            <span class="price-tag">¥{{ item.price }}</span>
            <div class="action-overlay">
              <el-button 
                type="danger" 
                size="small" 
                @click.stop="cancel(item.product_id)"
                :icon="Delete"
              >
                取消收藏
              </el-button>
            </div>
          </div>
          <div class="product-info">
            <h4 class="product-name">{{ item.title }}</h4>
            <div class="product-meta">
              <el-tag size="small" type="info">{{ item.category }}</el-tag>
              <div class="seller-info">
                <el-avatar :size="20" :src="item.seller.avatar">
                  {{ item.seller.nickname?.charAt(0) }}
                </el-avatar>
                <span class="seller-name">{{ item.seller.nickname }}</span>
              </div>
            </div>
            <span class="collect-time">{{ formatTime(item.created_at) }}</span>
          </div>
        </div>
        
        <el-empty v-if="favorites.length === 0 && !loading" description="暂无收藏" />
      </div>
      
      <div class="pagination" v-if="pagination.total > 0">
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
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Delete } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import { getMyFavoriteList, cancelFavorite } from '@/api/favorite'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const favorites = ref([])
const loading = ref(false)
const pagination = reactive({ page: 1, page_size: 10, total: 0 })

const loadData = async () => {
  loading.value = true
  try {
    const res = await getMyFavoriteList({ page: pagination.page, page_size: pagination.page_size })
    if (res.code === 200) {
      pagination.total = res.data.total
      favorites.value = res.data.list.map(item => ({
        favorite_id: item.favorite_id,
        product_id: item.product_id,
        title: item.title,
        price: item.price,
        category: item.category,
        created_at: item.created_at,
        cover: item.images && item.images.length ? item.images[0] : '',
        seller: item.seller || {}
      }))
    }
  } catch (error) {
    ElMessage.error('加载收藏列表失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (p) => {
  pagination.page = p
  loadData()
}

const goDetail = (id) => {
  router.push(`/product/${id}`)
}

const cancel = (productId) => {
  ElMessageBox.confirm('确定要取消收藏吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    const res = await cancelFavorite(productId)
    if (res.code === 200) {
      ElMessage.success('已取消收藏')
      loadData()
    } else {
      ElMessage.error(res.message || '取消失败')
    }
  }).catch(() => {})
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString()
}

onMounted(loadData)

</script>

<style scoped>
.favorites-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
}

.hero-section {
  padding: 120px 20px 40px;
  text-align: center;
  color: white;
}

.hero-section h1 {
  font-size: 48px;
  font-weight: bold;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.hero-section p {
  font-size: 18px;
  opacity: 0.95;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 0 20px;
}

.glass-card {
  background: var(--glass);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  overflow: hidden;
}

.glass-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 20px 0;
}

.product-card {
  padding: 0;
}

.product-image {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
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
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1976d2;
  font-size: 14px;
}

.price-tag {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 18px;
  box-shadow: 0 4px 12px rgba(238, 90, 111, 0.4);
}

.action-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .action-overlay {
  opacity: 1;
}

.product-info {
  padding: 16px;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.seller-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.seller-name {
  font-size: 12px;
  color: #666;
}

.collect-time {
  font-size: 12px;
  color: #999;
}

.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}
</style>
