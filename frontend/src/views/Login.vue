<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">校园交易平台</h2>
      
      <!-- 密码登录表单 -->
      <el-form 
        ref="passwordFormRef" 
        :model="passwordForm" 
        :rules="passwordRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="passwordForm.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="passwordForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            size="large"
            show-password
            @keyup.enter="handlePasswordLogin"
          />
        </el-form-item>

        <div class="form-footer">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
        </div>

        <el-button 
          type="primary" 
          size="large" 
          class="login-button"
          :loading="loading"
          @click="handlePasswordLogin"
        >
          登录
        </el-button>
      </el-form>

      <!-- 注册链接 -->
      <div class="register-link">
        还没有账号？
        <router-link to="/register">立即注册</router-link>
      </div>

      <div class="admin-link">
        <router-link to="/admin-login">管理员登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const store = useStore()
    const loading = ref(false)
    const rememberMe = ref(false)

    // 密码登录表单
    const passwordFormRef = ref(null)
    const passwordForm = reactive({
      username: '',
      password: ''
    })

    const validateAccount = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else {
        callback()
      }
    }

    const passwordRules = {
      username: [{ required: true, validator: validateAccount, trigger: 'blur' }],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
      ]
    }

    // 密码登录
    const handlePasswordLogin = () => {
      passwordFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            const response = await login(passwordForm)
            if (response.code === 200) {
              // 保存token和用户信息
              store.commit('SET_TOKEN', response.data.token)
              store.commit('SET_USER_INFO', response.data.user_info)
              
              ElMessage.success({
                message: '登录成功',
                duration: 1000
              })
              
              // 延迟跳转,让用户看到成功提示
              setTimeout(() => {
                router.push('/')
              }, 1000)
            } else {
              ElMessage.error(response.message)
            }
          } catch (error) {
            ElMessage.error('登录失败，请稍后重试')
          } finally {
            loading.value = false
          }
        }
      })
    }

    return {
      loading,
      rememberMe,
      passwordFormRef,
      passwordForm,
      passwordRules,
      handlePasswordLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
}

.login-form {
  margin-top: 20px;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  margin-top: 10px;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.admin-link {
  text-align: center;
  margin-top: 12px;
  font-size: 14px;
}

.admin-link a {
  color: #409eff;
  text-decoration: none;
}

.admin-link a:hover {
  text-decoration: underline;
}

.register-link a {
  color: #409eff;
  text-decoration: none;
  margin-left: 5px;
}

.register-link a:hover {
  text-decoration: underline;
}

:deep(.el-input__inner) {
  height: 45px;
  line-height: 45px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}
</style>
