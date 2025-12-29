<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">管理员登录</h2>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入管理员账号"
            prefix-icon="el-icon-user"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="login-button"
          :loading="loading"
          @click="handleLogin"
        >
          登录
        </el-button>
      </el-form>

      <div class="register-link">
        <router-link to="/login">返回用户登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminLogin } from '@/api/admin'

export default {
  name: 'AdminLogin',
  setup() {
    const router = useRouter()
    const loading = ref(false)

    const formRef = ref(null)
    const form = reactive({
      username: '',
      password: ''
    })

    const rules = {
      username: [{ required: true, message: '请输入管理员账号', trigger: 'blur' }],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
      ]
    }

    const handleLogin = () => {
      formRef.value.validate(async (valid) => {
        if (!valid) return
        loading.value = true
        try {
          const res = await adminLogin(form)
          if (res.code === 200) {
            localStorage.setItem('adminToken', res.data.token)
            localStorage.setItem('adminInfo', JSON.stringify(res.data.admin_info || {}))
            ElMessage.success({ message: '管理员登录成功', duration: 1000 })
            setTimeout(() => {
              router.push('/admin')
            }, 800)
          } else {
            ElMessage.error(res.message || '登录失败')
          }
        } catch (e) {
          ElMessage.error('登录失败，请检查账号密码')
        } finally {
          loading.value = false
        }
      })
    }

    return {
      loading,
      formRef,
      form,
      rules,
      handleLogin
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

.register-link a {
  color: #409eff;
  text-decoration: none;
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
