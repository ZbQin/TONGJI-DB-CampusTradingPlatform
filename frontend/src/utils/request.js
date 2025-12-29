import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: '/api',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 判断是否为管理端接口
    const isAdminAPI = config.url?.startsWith('/admin') || config.url?.startsWith('/report/list') || config.url?.startsWith('/report/handle') || config.url?.startsWith('/report/delete')
    
    // 管理端接口使用 adminToken，普通接口使用 token
    const token = isAdminAPI ? localStorage.getItem('adminToken') : localStorage.getItem('token')
    
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    // 确保 POST 请求使用 application/json
    if (config.method === 'post' && !config.headers['Content-Type']) {
      config.headers['Content-Type'] = 'application/json'
    }
    return config
  },
  error => {
    console.error('请求错误：', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data

    // 如果返回的状态码不是200，则认为是错误
    if (res.code !== 200) {
      // 401错误在登录/注册页面不显示提示
      const currentPath = router.currentRoute.value.path
      const isAuthPage = currentPath === '/login' || currentPath === '/register'
      const isAdminLoginPage = currentPath === '/admin-login'
      
      if (res.code === 401) {
        // 判断是否为管理端接口
        const isAdminAPI = response.config.url?.startsWith('/admin') || response.config.url?.startsWith('/report/list') || response.config.url?.startsWith('/report/handle') || response.config.url?.startsWith('/report/delete')
        
        if (isAdminAPI) {
          // 管理端401，清除管理员token
          localStorage.removeItem('adminToken')
          localStorage.removeItem('adminInfo')
          
          if (!isAdminLoginPage) {
            ElMessage({
              message: res.message || '管理员登录已过期，请重新登录',
              type: 'error',
              duration: 3000
            })
            router.push('/admin-login')
          }
        } else {
          // 普通用户401
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          
          if (!isAuthPage) {
            ElMessage({
              message: res.message || '未授权，请重新登录',
              type: 'error',
              duration: 3000
            })
            router.push('/login')
          }
        }
      } else {
        // 非401错误正常显示提示
        ElMessage({
          message: res.message || '请求失败',
          type: 'error',
          duration: 3000
        })
      }

      return Promise.reject(new Error(res.message || '请求失败'))
    } else {
      return res
    }
  },
  error => {
    console.error('响应错误：', error)
    
    let message = '网络错误，请稍后重试'
    const currentPath = router.currentRoute.value.path
    const isAuthPage = currentPath === '/login' || currentPath === '/register'
    const isAdminLoginPage = currentPath === '/admin-login'
    
    if (error.response) {
      // 判断是否为管理端接口
      const isAdminAPI = error.response.config.url?.startsWith('/admin') || error.response.config.url?.startsWith('/report/list') || error.response.config.url?.startsWith('/report/handle') || error.response.config.url?.startsWith('/report/delete')
      
      switch (error.response.status) {
        case 400:
          message = error.response.data.message || '请求参数错误'
          break
        case 401:
          message = isAdminAPI ? '管理员登录已过期，请重新登录' : '未授权，请重新登录'
          
          if (isAdminAPI) {
            localStorage.removeItem('adminToken')
            localStorage.removeItem('adminInfo')
            if (!isAdminLoginPage) {
              router.push('/admin-login')
            }
          } else {
            localStorage.removeItem('token')
            localStorage.removeItem('userInfo')
            if (!isAuthPage) {
              router.push('/login')
            }
          }
          break
        case 403:
          message = '没有权限访问'
          break
        case 404:
          message = '请求资源不存在'
          break
        case 500:
          message = '服务器错误'
          break
        default:
          message = error.response.data.message || '请求失败'
      }
    }

    // 在登录/注册/管理员登录页面且是401错误时不显示提示
    if (!((isAuthPage || isAdminLoginPage) && error.response?.status === 401)) {
      ElMessage({
        message: message,
        type: 'error',
        duration: 3000
      })
    }

    return Promise.reject(error)
  }
)

export default service
