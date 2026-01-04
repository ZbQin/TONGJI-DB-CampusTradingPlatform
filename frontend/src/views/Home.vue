<template>
  <div class="home-container">
    <NavBar />

    <div class="page-shell">
      <section class="hero-shell home-hero">
        <div class="hero-search">
          <el-input
            v-model="searchQuery"
            placeholder="输入关键词搜索"
            class="search-input"
            :prefix-icon="Search"
            clearable
          >
            <template #append>
              <el-button type="primary" :icon="Search" @click="loadProducts" />
            </template>
          </el-input>
          <div class="quick-filters">
            <div
              v-for="cat in categories"
              :key="cat.category_id"
              class="pill"
              :class="{ active: selectedCategoryId === cat.category_id }"
              @click="selectedCategoryId = cat.category_id"
            >
              {{ cat.name }}
            </div>
          </div>
        </div>
      </section>

      <section class="soft-card glass listing-card">
        <div class="section-header">
          <div>
            <h2 class="section-title">最新上架</h2>
            <p class="section-sub">好物即刻浏览，支持筛选和搜索</p>
          </div>
          <el-button class="ghost-button" @click="loadProducts">刷新</el-button>
        </div>

        <el-skeleton v-if="loading" :rows="3" animated />

        <div v-else class="product-grid">
          <el-card
            v-for="item in products"
            :key="item.id"
            class="product-card"
            :body-style="{ padding: '0px' }"
            shadow="hover"
            @click="goToDetail(item.id)"
          >
            <div class="image-placeholder">
              <img v-if="item.image" :src="item.image" class="product-image" />
              <div v-else class="no-image">暂无图片</div>
              <div class="price-chip">¥ {{ item.price }}</div>
            </div>
            <div class="product-info">
              <h3 class="product-title">{{ item.title }}</h3>
              <div class="product-meta">
                <span class="seller-name">{{ item.seller }}</span>
                <span class="publish-time">{{ item.time }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import NavBar from '@/components/NavBar.vue'
import { Search } from '@element-plus/icons-vue'
import { getProductList } from '@/api/product'
import { getCategoryList } from '@/api/category'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useStore()
const searchQuery = ref('')
const selectedCategoryId = ref(null)
const products = ref([])
const loading = ref(false)
const categories = ref([])
const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

// 加载分类列表
const loadCategories = async () => {
  try {
    const res = await getCategoryList()
    if (res.code === 200) {
      // 添加“全部”到分类列表前面
      categories.value = [
        { category_id: null, name: '全部' },
        ...res.data
      ]
    }
  } catch (error) {
    ElMessage.error('加载分类列表失败')
  }
}

// 加载商品列表
const loadProducts = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchQuery.value || undefined,
      category_id: selectedCategoryId.value,
      sort: 'latest'
    }
    
    const res = await getProductList(params)
    if (res.code === 200) {
      products.value = res.data.list.map(item => ({
        id: item.product_id,
        title: item.title,
        price: item.price,
        seller: item.seller.nickname,
        time: formatTime(item.created_at),
        image: item.images && item.images.length > 0 ? item.images[0] : ''
      }))
      pagination.total = res.data.total
    }
  } catch (error) {
    ElMessage.error('加载商品列表失败')
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  // 后端返回的是UTC时间，需要正确解析
  const time = new Date(timeStr + (timeStr.includes('Z') ? '' : ' UTC'))
  const now = new Date()
  const diff = Math.floor((now - time) / 1000)
  
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  if (diff < 2592000) return `${Math.floor(diff / 86400)}天前`
  return timeStr.split(' ')[0]
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

// 监听分类和搜索变化
watch([selectedCategoryId, searchQuery], () => {
  pagination.page = 1
  loadProducts()
})

onMounted(() => {
  loadCategories()
  loadProducts()
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: var(--bg-page);
}
.home-hero {
  margin-bottom: 22px;
}
.hero-search {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 900px;
}
.search-input {
  max-width: 640px;
}
.quick-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.pill {
  transition: all 0.2s ease;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.4);
}

.pill.active {
  background: #fff;
  color: var(--primary-strong);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.listing-card {
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 18px;
}

.product-card {
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  border-radius: 16px;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 35px rgba(34, 61, 255, 0.15);
}

.image-placeholder {
  height: 200px;
  background: linear-gradient(135deg, #f7f9ff, #f0f4ff);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: var(--muted);
}

.product-info {
  padding: 14px 14px 16px;
}

.product-title {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--muted);
}

.price-chip {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #fff;
  color: var(--primary-strong);
  padding: 6px 10px;
  border-radius: 12px;
  font-weight: 700;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
}

@media (max-width: 960px) {
  .home-hero {
    grid-template-columns: 1fr;
  }
  .hero-visual {
    justify-content: flex-start;
  }
}
</style>
