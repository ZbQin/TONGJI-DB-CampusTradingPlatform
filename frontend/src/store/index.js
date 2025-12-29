import { createStore } from 'vuex'
import { getUserInfo, logout } from '@/api/auth'

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}')
  },
  
  getters: {
    isLoggedIn: state => !!state.token,
    userInfo: state => state.userInfo,
    userId: state => state.userInfo.user_id,
    username: state => state.userInfo.username,
    nickname: state => state.userInfo.nickname,
    avatar: state => state.userInfo.avatar
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    
    CLEAR_USER_DATA(state) {
      state.token = ''
      state.userInfo = {}
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  },
  
  actions: {
    // 获取用户信息
    async fetchUserInfo({ commit }) {
      try {
        const response = await getUserInfo()
        if (response.code === 200) {
          commit('SET_USER_INFO', response.data)
          return response.data
        }
      } catch (error) {
        console.error('获取用户信息失败：', error)
        throw error
      }
    },
    
    // 退出登录
    async logout({ commit }) {
      try {
        await logout()
      } catch (error) {
        console.error('退出登录失败：', error)
      } finally {
        commit('CLEAR_USER_DATA')
      }
    }
  }
})
