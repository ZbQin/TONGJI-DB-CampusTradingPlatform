<template>
  <div class="user-profile-container">
    <NavBar />
    
    <div class="profile-content">
      <!-- 用户信息卡片 -->
      <div class="user-info-card glass-card">
        <div class="user-header">
          <el-avatar :size="100" :src="userInfo.avatar" class="user-avatar">
            {{ userInfo.username?.charAt(0).toUpperCase() }}
          </el-avatar>
          <div class="user-basic">
            <h2 class="username">{{ userInfo.username }}</h2>
            <div class="user-meta">
              <el-tag type="info" size="small">学号: {{ userInfo.student_id }}</el-tag>
              <el-tag type="success" size="small" v-if="userInfo.phone">{{ userInfo.phone }}</el-tag>
            </div>
          </div>
        </div>
        
        <!-- 评分统计 -->
        <div class="rating-section">
          <div class="rating-display">
            <div class="avg-rating">
              <span class="rating-number">{{ formatRating(ratingStats.avg_rating) }}</span>
              <el-rate 
                :model-value="ratingStats.avg_rating || 0" 
                disabled 
                text-color="#409eff"
                :texts="['极差', '失望', '一般', '满意', '惊喜']"
              />
            </div>
            <div class="review-count">
              <el-icon><ChatDotSquare /></el-icon>
              <span>{{ ratingStats.review_count || 0 }} 条评价</span>
            </div>
          </div>
          
          <el-button 
            type="primary" 
            @click="openReviewModal"
            v-if="!isCurrentUser"
            class="review-btn"
          >
            <el-icon><EditPen /></el-icon>
            评价用户
          </el-button>
          <el-button
            :type="isFollowing ? 'success' : 'primary'"
            @click="toggleFollow"
            v-if="!isCurrentUser"
            class="follow-btn"
          >
            {{ isFollowing ? '已关注' : '关注' }} ({{ followerCount }})
          </el-button>
        </div>
      </div>
      
      <!-- 标签页 -->
      <el-tabs v-model="activeTab" class="profile-tabs">
        <el-tab-pane label="发布的商品" name="products">
          <div class="products-grid" v-if="userProducts.length > 0">
            <div 
              class="product-card glass-card" 
              v-for="product in userProducts" 
              :key="product.product_id"
              @click="goToProductDetail(product.product_id)"
            >
              <div class="product-image">
                <img :src="product.image_url || '/placeholder.png'" :alt="product.product_name" />
                <span class="price-tag">¥{{ product.price }}</span>
              </div>
              <div class="product-info">
                <h4 class="product-name">{{ product.product_name }}</h4>
                <p class="product-desc">{{ product.description }}</p>
                <div class="product-meta">
                  <el-tag size="small" type="info">{{ product.condition }}</el-tag>
                  <span class="time">{{ formatTime(product.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无发布商品" />
        </el-tab-pane>
        
        <el-tab-pane label="收到的评价" name="reviews">
          <div class="reviews-list" v-if="receivedReviews.length > 0">
            <div 
              class="review-card glass-card" 
              v-for="review in receivedReviews" 
              :key="review.review_id"
            >
              <div class="review-header">
                <div class="reviewer-info">
                  <el-avatar :size="40">{{ review.reviewer_username?.charAt(0) }}</el-avatar>
                  <span class="reviewer-name">{{ review.reviewer_username }}</span>
                </div>
                <el-rate :model-value="review.rating || 0" disabled />
              </div>
              <p class="review-comment">{{ review.comment }}</p>
              <span class="review-time">{{ formatTime(review.created_at) }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无评价" />
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 评价对话框 -->
    <ReviewModal 
      v-if="showReviewModal"
      :visible="showReviewModal"
      :reviewee-id="userId"
      :reviewee-name="userInfo.username"
      @close="showReviewModal = false"
      @success="handleReviewSuccess"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { ChatDotSquare, EditPen } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import ReviewModal from '@/components/ReviewModal.vue'
import { getUserProducts } from '@/api/product'
import { getUserRatingStats, getReviewsByReviewee } from '@/api/review'
import { addFollow, cancelFollow, checkFollowing, getFollowStats } from '@/api/follow'

export default {
  name: 'UserProfile',
  components: {
    NavBar,
    ReviewModal,
    ChatDotSquare,
    EditPen
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const store = useStore()
    
    const userId = ref(parseInt(route.params.id))
    const userInfo = ref({})
    const userProducts = ref([])
    const receivedReviews = ref([])
    const ratingStats = ref({})
    const activeTab = ref('products')
    const showReviewModal = ref(false)
    
    const isCurrentUser = computed(() => {
      return userId.value === store.state.userInfo?.user_id
    })
    
    const fetchUserInfo = async () => {
      try {
        // 从商品列表中获取用户信息
        const res = await getUserProducts(userId.value)
        if (res.code === 200 && res.data.list && res.data.list.length > 0) {
          const firstProduct = res.data.list[0]
          userInfo.value = {
            user_id: userId.value,
            username: firstProduct.seller?.nickname || firstProduct.seller?.username || '未知用户',
            student_id: firstProduct.seller?.student_id || '',
            phone: firstProduct.seller?.phone || ''
          }
          userProducts.value = res.data.list || []
        } else {
          // 如果没有商品，设置基本用户信息
          userInfo.value = {
            user_id: userId.value,
            username: '用户' + userId.value,
            student_id: '',
            phone: ''
          }
          userProducts.value = []
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        // 即使出错也设置基本信息
        userInfo.value = {
          user_id: userId.value,
          username: '用户' + userId.value,
          student_id: '',
          phone: ''
        }
        userProducts.value = []
      }
    }
    
    const fetchRatingStats = async () => {
      try {
        const res = await getUserRatingStats(userId.value)
        ratingStats.value = res.data
      } catch (error) {
        console.error('获取评分统计失败:', error)
      }
    }
    
    const fetchReceivedReviews = async () => {
      try {
        const res = await getReviewsByReviewee(userId.value)
        // 后端返回 data.list 或者 data.reviews，做兼容处理
        const list = (res.data && (res.data.list || res.data.reviews)) || []
        receivedReviews.value = list.map(item => ({
          review_id: item.review_id,
          rating: item.rating,
          comment: item.content || item.comment || '',
          created_at: item.created_at,
          reviewer_username: item.reviewer_nickname || item.reviewer_username || '匿名',
          reviewer_avatar: item.reviewer_avatar || ''
        }))
      } catch (error) {
        console.error('获取评价列表失败:', error)
      }
    }

    const openReviewModal = () => {
      if (!store.state.token) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      showReviewModal.value = true
    }

    // 关注相关
    const isFollowing = ref(false)
    const followerCount = ref(0)

    const fetchFollowInfo = async () => {
      try {
        const res = await checkFollowing(userId.value)
        isFollowing.value = res.data?.is_following || false
      } catch (error) {
        console.error('检查关注状态失败', error)
      }

      try {
        const sres = await getFollowStats(userId.value)
        followerCount.value = sres.data?.followers_count || 0
      } catch (error) {
        console.error('获取关注统计失败', error)
      }
    }

    const toggleFollow = async () => {
      if (!store.state.token) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }

      try {
        if (isFollowing.value) {
          const res = await cancelFollow(userId.value)
          if (res.code === 200) {
            isFollowing.value = false
            followerCount.value = Math.max(0, followerCount.value - 1)
            ElMessage.success('已取消关注')
          }
        } else {
          const res = await addFollow(userId.value)
          if (res.code === 200) {
            isFollowing.value = true
            followerCount.value = followerCount.value + 1
            ElMessage.success('已关注')
          }
        }
      } catch (error) {
        console.error('关注操作失败', error)
        ElMessage.error('操作失败')
      }
    }
    
    const handleReviewSuccess = () => {
      showReviewModal.value = false
      fetchRatingStats()
      fetchReceivedReviews()
      ElMessage.success('评价成功')
    }
    
    const goToProductDetail = (productId) => {
      router.push(`/product/${productId}`)
    }
    
    const formatRating = (rating) => {
      if (!rating) return '0.0'
      return Number(rating).toFixed(1)
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
    
    onMounted(() => {
      fetchUserInfo()
      fetchRatingStats()
      fetchReceivedReviews()
      fetchFollowInfo()
    })
    
    return {
      userId,
      userInfo,
      userProducts,
      receivedReviews,
      ratingStats,
      activeTab,
      showReviewModal,
      isCurrentUser,
      openReviewModal,
      handleReviewSuccess,
      goToProductDetail,
      formatRating,
      formatTime,
      isFollowing,
      followerCount,
      toggleFollow
    }
  }
}
</script>

<style scoped>
.user-profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
}

.profile-content {
  max-width: 1200px;
  margin: 80px auto 0;
  padding: 24px;
}

.glass-card {
  background: var(--glass);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.user-info-card {
  padding: 32px;
  margin-bottom: 24px;
}

.user-header {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.user-avatar {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
  font-size: 36px;
  font-weight: bold;
}

.user-basic {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
}

.username {
  font-size: 28px;
  font-weight: bold;
  color: #1976d2;
  margin: 0;
}

.user-meta {
  display: flex;
  gap: 12px;
}

.rating-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 24px;
  border-top: 1px solid rgba(25, 118, 210, 0.1);
}

.rating-display {
  display: flex;
  gap: 32px;
  align-items: center;
}

.avg-rating {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rating-number {
  font-size: 48px;
  font-weight: bold;
  color: #2196f3;
  line-height: 1;
}

.review-count {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #666;
}

.review-btn {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  border: none;
  padding: 12px 32px;
  font-size: 16px;
}

.profile-tabs {
  background: var(--glass);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.product-card {
  cursor: pointer;
  overflow: hidden;
  padding: 0;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
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

.product-info {
  padding: 16px;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-desc {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time {
  font-size: 12px;
  color: #999;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px 0;
}

.review-card {
  padding: 20px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.reviewer-name {
  font-weight: bold;
  color: #333;
}

.review-comment {
  color: #666;
  line-height: 1.6;
  margin: 12px 0;
}

.review-time {
  font-size: 12px;
  color: #999;
}

.follow-btn {
  margin-left: 12px;
}


:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.el-tabs__item) {
  color: #666;
  font-size: 16px;
}

:deep(.el-tabs__item.is-active) {
  color: #2196f3;
}

:deep(.el-tabs__active-bar) {
  background-color: #2196f3;
}
</style>
