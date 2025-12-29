<template>
  <div class="layout-container">
    <!-- 顶部导航栏 -->
    <div class="top-nav">
      <div class="brand">校园交易平台</div>
      <div class="nav-links">
        <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          :ellipsis="false"
          router
          class="nav-menu"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/publish">发布商品</el-menu-item>
          <el-menu-item index="/wanted">求购广场</el-menu-item>
          <el-menu-item index="/wanted/publish">发布求购</el-menu-item>
          <el-menu-item index="/chat">
            <el-badge :value="unreadCount" :hidden="unreadCount === 0">
              消息
            </el-badge>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="user-block">
        <el-dropdown trigger="click">
          <span class="user-trigger">
            <el-avatar :size="32" :src="userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
            <span class="user-name">{{ userInfo.nickname || userInfo.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click.native="$router.push('/profile')">个人中心</el-dropdown-item>
              <el-dropdown-item @click.native="$router.push('/follows')">我的关注/粉丝</el-dropdown-item>
              <el-dropdown-item divided @click.native="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 左侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <el-avatar :size="60" :src="userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
        <div class="user-info">
          <div class="nickname">{{ userInfo.nickname || userInfo.username }}</div>
        </div>
      </div>
      
      <el-menu
        :default-active="activeIndex"
        class="sidebar-menu"
        router
      >
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
        <el-menu-item index="/my-items">
          <el-icon><Goods /></el-icon>
          <span>我的发布</span>
        </el-menu-item>
        <el-menu-item index="/favorites">
          <el-icon><Star /></el-icon>
          <span>我的收藏</span>
        </el-menu-item>
        <el-menu-item index="/follows">
          <el-icon><UserFilled /></el-icon>
          <span>我的关注/粉丝</span>
        </el-menu-item>
        <el-menu-item index="/wanted/my-list">
          <el-icon><Document /></el-icon>
          <span>我的求购</span>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { User, Goods, Star, UserFilled, Document } from '@element-plus/icons-vue'
import { getUnreadCount } from '@/api/chat'

const router = useRouter()
const route = useRoute()
const store = useStore()

const activeIndex = computed(() => route.path)
const userInfo = computed(() => store.getters.userInfo)
const unreadCount = ref(0)

// 加载未读消息数
const loadUnreadCount = async () => {
  try {
    const res = await getUnreadCount()
    if (res.code === 200) {
      const total = res.data.sessions?.reduce((sum, s) => sum + s.unread_count, 0) || 0
      unreadCount.value = total
    }
  } catch (error) {
    console.error('获取未读消息数失败', error)
  }
}

const handleLogout = async () => {
  await store.dispatch('logout')
  ElMessage.success('退出成功')
  router.push('/login')
}

onMounted(() => {
  loadUnreadCount()
  // 定时刷新未读消息数
  setInterval(loadUnreadCount, 30000) // 每30秒刷新一次
})
</script>
<style scoped>
.layout-container {
  position: relative;
}

/* 顶部导航栏 */
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: grid;
  grid-template-columns: 220px 1fr auto;
  align-items: center;
  padding: 12px 24px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
}

.brand {
  font-size: 20px;
  font-weight: 800;
  color: var(--primary);
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  justify-content: center;
}

.nav-menu {
  border-bottom: none;
}

.user-block {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
}

.user-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-strong);
  font-weight: 600;
}

.user-name {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 左侧边栏 */
.sidebar {
  position: fixed;
  left: 0;
  top: 64px;
  bottom: 0;
  width: 240px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid var(--border);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  z-index: 90;
}

.sidebar-header {
  padding: 24px 20px;
  text-align: center;
  border-bottom: 1px solid var(--border);
}

.user-info {
  margin-top: 12px;
}

.nickname {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-strong);
}

.sidebar-menu {
  border-right: none;
  padding: 12px 0;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 4px 12px;
  border-radius: 8px;
  transition: all 0.3s;
}

.sidebar-menu .el-menu-item:hover {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.08), rgba(25, 118, 210, 0.12));
}

.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.15), rgba(25, 118, 210, 0.2));
  color: #2196f3;
  font-weight: 600;
}

.sidebar-menu .el-icon {
  font-size: 18px;
  margin-right: 8px;
}

@media (max-width: 960px) {
  .top-nav {
    grid-template-columns: 1fr auto;
    grid-template-rows: auto auto;
    row-gap: 8px;
  }
  .nav-links {
    grid-column: 1 / -1;
    justify-content: flex-start;
  }
  .sidebar {
    display: none;
  }
}
</style>
