<template>
  <div class="detail-container">
    <NavBar />
    <div class="page-shell">
      <el-card class="product-detail-card soft-card glass">
        <div class="product-layout">
          <!-- 左侧图片 -->
          <div class="image-section">
            <div class="main-image">
              <img v-if="product.image" :src="product.image" />
              <div v-else class="no-image">暂无图片</div>
            </div>
          </div>
          
          <!-- 右侧信息 -->
          <div class="info-section">
            <div class="floating-badge">精选好物</div>
            <h1 class="title">{{ product.title }}</h1>

            <div class="price-box">
              <div class="currency">¥</div>
              <div class="price">{{ product.price }}</div>
              <el-tag size="small" class="status-tag">安全交易</el-tag>
            </div>
            
            <div class="meta-info">
              <div class="meta-item seller-card" @click="goToUserProfile">
                <el-avatar :size="40" class="seller-avatar">
                  {{ product.seller?.charAt(0) }}
                </el-avatar>
                <div class="seller-info">
                  <span class="label">卖家：</span>
                  <span class="value seller-name">{{ product.seller }}</span>
                  <el-icon class="arrow-icon"><ArrowRight /></el-icon>
                </div>
              </div>
              <div class="meta-item">
                <span class="label">发布时间：</span>
                <span class="value">{{ product.time }}</span>
              </div>
              <div class="meta-item">
                <span class="label">分类：</span>
                <el-tag size="small">{{ product.category }}</el-tag>
              </div>
            </div>
            
            <div class="description-box">
              <div class="label">商品详情：</div>
              <div class="content">{{ product.description }}</div>
            </div>
            
            <div class="action-buttons">
              <el-button type="primary" size="large" @click="handleContact">联系卖家</el-button>
              <el-button size="large" @click="handleCollect">
                {{ isFavorited ? '已收藏' : '收藏商品' }}
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowRight } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import { ElMessage } from 'element-plus'
import { getProductDetail } from '@/api/product'
import { getOrCreateSession } from '@/api/chat'
import { addFavorite, cancelFavorite, checkFavorite } from '@/api/favorite'

const route = useRoute()
const router = useRouter()
const product = ref({})
const loading = ref(false)
const isFavorited = ref(false)

onMounted(async () => {
  const id = route.params.id
  loading.value = true
  try {
    const res = await getProductDetail(id)
    if (res.code === 200) {
      const data = res.data
      product.value = {
        id: data.product_id,
        title: data.title,
        price: data.price,
        seller: data.seller.nickname,
        sellerId: data.seller.user_id,
        time: data.created_at,
        category: data.category,
        description: data.description,
        image: data.images && data.images.length > 0 ? data.images[0].image_url : ''
      }

      // 检查收藏状态
      const checkRes = await checkFavorite(product.value.id)
      if (checkRes.code === 200) {
        isFavorited.value = checkRes.data.is_favorited
      }
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('加载商品详情失败')
  } finally {
    loading.value = false
  }
})

const handleContact = async () => {
  try {
    const res = await getOrCreateSession({
      product_id: product.value.id,
      seller_id: product.value.sellerId
    })
    
    if (res.code === 200) {
      // 跳转到聊天页面
      router.push('/chat')
      ElMessage.success('已为您创建会话')
    } else {
      ElMessage.error(res.message || '创建会话失败')
    }
  } catch (error) {
    ElMessage.error('创建会话失败')
  }
}

const handleCollect = async () => {
  if (!product.value.id) return
  try {
    if (isFavorited.value) {
      const res = await cancelFavorite(product.value.id)
      if (res.code === 200) {
        isFavorited.value = false
        ElMessage.success('已取消收藏')
      } else {
        ElMessage.error(res.message || '取消收藏失败')
      }
    } else {
      const res = await addFavorite(product.value.id)
      if (res.code === 200) {
        isFavorited.value = true
        ElMessage.success('收藏成功')
      } else {
        ElMessage.error(res.message || '收藏失败')
      }
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const goToUserProfile = () => {
  if (product.value.sellerId) {
    router.push(`/user/${product.value.sellerId}`)
  }
}
</script>

<style scoped>
.detail-container {
  min-height: 100vh;
  background: var(--bg-page);
}

.page-shell {
  padding-top: 20px;
}

.product-layout {
  display: flex;
  gap: 40px;
}

.image-section {
  flex: 1;
  max-width: 400px;
}

.main-image {
  width: 100%;
  height: 400px;
  background: linear-gradient(135deg, #f4f7ff, #eef3ff);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--card-shadow);
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: #909399;
}

.info-section {
  flex: 1;
}

.title {
  font-size: 26px;
  color: var(--text-strong);
  margin: 6px 0 20px;
}

.price-box {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  background: linear-gradient(135deg, #ffe3eb, #fff4ec);
  padding: 12px 16px;
  border-radius: 14px;
  margin-bottom: 20px;
  color: #f56c6c;
  box-shadow: 0 12px 30px rgba(255, 129, 163, 0.18);
}

.currency {
  font-size: 20px;
  font-weight: bold;
}

.price {
  font-size: 32px;
  font-weight: bold;
  margin-left: 5px;
}

.status-tag {
  background: rgba(19, 194, 194, 0.16);
  color: #0f9cbf;
  border-color: transparent;
}

.meta-info {
  margin-bottom: 30px;
}

.meta-item {
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--text-normal);
}

.meta-item .label {
  color: var(--muted);
  margin-right: 10px;
}

.seller-card {
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

.seller-card:hover {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(25, 118, 210, 0.15));
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
}

.seller-avatar {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
  font-weight: bold;
}

.seller-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.seller-name {
  color: #2196f3;
  font-weight: bold;
}

.arrow-icon {
  color: #2196f3;
  margin-left: auto;
}

.description-box {
  margin-bottom: 30px;
  border-top: 1px solid var(--border);
  padding-top: 20px;
}

.description-box .label {
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--text-strong);
}

.description-box .content {
  line-height: 1.6;
  color: var(--text-normal);
}

.action-buttons {
  display: flex;
  gap: 20px;
}

@media (max-width: 768px) {
  .product-layout {
    flex-direction: column;
  }
  
  .image-section {
    max-width: 100%;
  }
  
  .main-image {
    height: 300px;
  }
}
</style>