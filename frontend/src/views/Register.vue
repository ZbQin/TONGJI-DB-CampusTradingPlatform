<template>
  <div class="register-container">
    <div class="register-box">
      <h2 class="register-title">用户注册</h2>
      
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules"
        class="register-form"
        label-width="0"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名 (3-20个字符)"
            prefix-icon="el-icon-user"
            size="large"
            maxlength="20"
          />
        </el-form-item>

        <el-form-item prop="nickname">
          <el-input
            v-model="form.nickname"
            placeholder="请输入昵称 (2-20个字符)"
            prefix-icon="el-icon-edit"
            size="large"
            maxlength="20"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码 (6-20个字符)"
            prefix-icon="el-icon-lock"
            size="large"
            show-password
            maxlength="20"
          />
        </el-form-item>

        <el-form-item prop="confirm_password">
          <el-input
            v-model="form.confirm_password"
            type="password"
            placeholder="请确认密码"
            prefix-icon="el-icon-lock"
            size="large"
            show-password
            maxlength="20"
            @keyup.enter="handleRegister"
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="agreeTerms">
            我已阅读并同意
            <a href="#" @click.prevent="showTerms = true">《用户协议》</a>
            和
            <a href="#" @click.prevent="showPrivacy = true">《隐私政策》</a>
          </el-checkbox>
        </el-form-item>

        <el-button 
          type="primary" 
          size="large" 
          class="register-button"
          :loading="loading"
          @click="handleRegister"
        >
          注册
        </el-button>
      </el-form>

      <div class="login-link">
        已有账号？
        <router-link to="/login">立即登录</router-link>
      </div>
    </div>

    <!-- 用户协议对话框 -->
    <el-dialog title="用户协议" v-model="showTerms" width="600px">
      <div class="terms-content">
        <h3>欢迎使用校园交易平台</h3>
        <p>在使用本平台前，请仔细阅读以下条款...</p>
        <p>1. 用户应当遵守国家法律法规...</p>
        <p>2. 用户应当保证账户信息的真实性...</p>
        <p>3. 禁止发布违规商品信息...</p>
        <!-- 更多条款内容 -->
      </div>
    </el-dialog>

    <!-- 隐私政策对话框 -->
    <el-dialog title="隐私政策" v-model="showPrivacy" width="600px">
      <div class="terms-content">
        <h3>隐私保护声明</h3>
        <p>我们重视您的隐私保护...</p>
        <p>1. 我们会收集的信息...</p>
        <p>2. 信息的使用方式...</p>
        <p>3. 信息的保护措施...</p>
        <!-- 更多隐私政策内容 -->
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const formRef = ref(null)
    const loading = ref(false)
    const agreeTerms = ref(false)
    const showTerms = ref(false)
    const showPrivacy = ref(false)

    const form = reactive({
      username: '',
      nickname: '',
      password: '',
      confirm_password: ''
    })

    // 表单验证规则
    const validateUsername = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else if (value.length < 3 || value.length > 20) {
        callback(new Error('用户名长度为3-20个字符'))
      } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
        callback(new Error('用户名只能包含字母、数字和下划线'))
      } else {
        callback()
      }
    }

    const validateConfirmPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请再次输入密码'))
      } else if (value !== form.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    const rules = {
      username: [
        { required: true, validator: validateUsername, trigger: 'blur' }
      ],
      nickname: [
        { required: true, message: '请输入昵称', trigger: 'blur' },
        { min: 2, max: 20, message: '昵称长度为2-20个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
      ],
      confirm_password: [
        { required: true, validator: validateConfirmPassword, trigger: 'blur' }
      ]
    }

    // 注册
    const handleRegister = () => {
      if (!agreeTerms.value) {
        ElMessage.warning('请先阅读并同意用户协议和隐私政策')
        return
      }

      formRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            const response = await register({
              username: form.username,
              nickname: form.nickname,
              password: form.password
            })

            if (response.code === 200) {
              ElMessage.success('注册成功，即将跳转到登录页')
              setTimeout(() => {
                router.push('/login')
              }, 1500)
            } else {
              ElMessage.error(response.message)
            }
          } catch (error) {
            ElMessage.error('注册失败，请稍后重试')
          } finally {
            loading.value = false
          }
        }
      })
    }

    return {
      formRef,
      form,
      rules,
      loading,
      agreeTerms,
      showTerms,
      showPrivacy,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-box {
  width: 450px;
  padding: 40px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.register-title {
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
}

.register-form {
  margin-top: 20px;
}

.register-button {
  width: 100%;
  margin-top: 10px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.login-link a {
  color: #409eff;
  text-decoration: none;
  margin-left: 5px;
}

.login-link a:hover {
  text-decoration: underline;
}

.terms-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  line-height: 1.8;
}

.terms-content h3 {
  margin-bottom: 15px;
  color: #333;
}

.terms-content p {
  margin-bottom: 10px;
  color: #666;
}

:deep(.el-input__inner) {
  height: 45px;
  line-height: 45px;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-checkbox) {
  font-size: 14px;
}

:deep(.el-checkbox a) {
  color: #409eff;
  text-decoration: none;
}

:deep(.el-checkbox a:hover) {
  text-decoration: underline;
}
</style>
