import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/admin-login',
    name: 'AdminLogin',
    component: () => import('@/views/AdminLogin.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: () => import('@/views/AdminPanel.vue'),
    meta: { requiresAuth: false, requiresAdmin: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/publish',
    name: 'Publish',
    component: () => import('@/views/Publish.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-items',
    name: 'MyItems',
    component: () => import('@/views/MyItems.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/Favorites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/follows',
    name: 'Follows',
    component: () => import('@/views/Follows.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wanted',
    name: 'WantedList',
    component: () => import('@/views/WantedList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wanted/detail/:id',
    name: 'WantedDetail',
    component: () => import('@/views/WantedDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wanted/publish',
    name: 'WantedPublish',
    component: () => import('@/views/WantedPublish.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wanted/my-list',
    name: 'MyWanted',
    component: () => import('@/views/MyWanted.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/:id',
    name: 'UserProfile',
    component: () => import('@/views/UserProfile.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const adminToken = localStorage.getItem('adminToken')
  
  // 如果路由需要管理员权限
  if (to.meta.requiresAdmin) {
    if (adminToken) {
      next()
    } else {
      next('/admin-login')
    }
    return
  }
  
  // 如果路由需要认证
  if (to.meta.requiresAuth) {
    if (token) {
      next()
    } else {
      next('/login')
    }
  } else {
    // 如果已登录，访问登录/注册页，则跳转到首页
    if (token && (to.path === '/login' || to.path === '/register')) {
      next('/')
    } else if (adminToken && to.path === '/admin-login') {
      // 如果管理员已登录，访问管理员登录页，则跳转到管理后台
      next('/admin')
    } else {
      next()
    }
  }
})

export default router
