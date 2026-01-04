<template>
  <div class="profile-container">
    <NavBar />
    <div class="page-shell">
      <div class="hero-shell profile-hero">
        <div>
          <div class="floating-badge">完善资料 · 信任加分</div>
          <h2>你的校园名片</h2>
          <p class="section-sub">更新头像、昵称和校区信息，让同学更快信任你</p>
        </div>
        <el-button class="ghost-button" @click="$router.back()">返回</el-button>
      </div>

      <el-card class="box-card soft-card glass">
      <template #header>
        <div class="card-header">
          <span>个人中心</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="info">
          <div class="user-info-form">
            <el-form :model="userInfo" label-width="100px">
              <el-form-item label="头像">
                <el-upload
                  class="avatar-uploader"
                  action=""
                  :show-file-list="false"
                  :http-request="handleAvatarUpload"
                  :before-upload="beforeAvatarUpload"
                >
                  <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" />
                  <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                </el-upload>
              </el-form-item>
              
              <el-form-item label="用户名">
                <el-input v-model="userInfo.username" disabled></el-input>
              </el-form-item>
              
              <el-form-item label="昵称">
                <el-input v-model="userInfo.nickname"></el-input>
              </el-form-item>
              
              <el-form-item label="个人简介">
                <el-input type="textarea" v-model="userInfo.bio"></el-input>
              </el-form-item>
              
              <el-form-item label="校区">
                <el-select v-model="userInfo.campus" placeholder="请选择校区">
                  <el-option label="四平路校区" value="四平路校区"></el-option>
                  <el-option label="嘉定校区" value="嘉定校区"></el-option>
                  <el-option label="沪西校区" value="沪西校区"></el-option>
                  <el-option label="彰武校区" value="彰武校区"></el-option>
                </el-select>
              </el-form-item>
              
              <el-form-item label="宿舍楼">
                <el-input v-model="userInfo.dormitory"></el-input>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleUpdateProfile">保存修改</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
        
        <!-- 修改密码 -->
        <el-tab-pane label="修改密码" name="password">
          <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
            <el-form-item label="原密码" prop="old_password">
              <el-input type="password" v-model="passwordForm.old_password" show-password></el-input>
            </el-form-item>
            
            <el-form-item label="新密码" prop="new_password">
              <el-input type="password" v-model="passwordForm.new_password" show-password></el-input>
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="confirm_password">
              <el-input type="password" v-model="passwordForm.confirm_password" show-password></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'
import { getUserInfo, updateProfile, changePassword, uploadAvatar } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'

const activeTab = ref('info')
const userInfo = ref({
  username: '',
  nickname: '',
  bio: '',
  campus: '',
  dormitory: '',
  avatar: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const passwordFormRef = ref(null)
const store = useStore()

const passwordRules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const res = await getUserInfo()
    if (res.code === 200) {
      userInfo.value = res.data
      // 同步全局用户信息，确保导航栏等位置头像一致
      store.commit('SET_USER_INFO', res.data)
      // 处理头像URL，如果是相对路径，可能需要拼接后端地址
      // 这里假设后端返回的是 /static/... 这样的路径
      // 如果前端和后端在不同端口，可能需要拼接 baseURL
      // 暂时直接使用，假设配置了代理或者已经是完整URL
    }
  } catch (error) {
    console.error(error)
  }
}

// 更新个人信息
const handleUpdateProfile = async () => {
  try {
    const res = await updateProfile(userInfo.value)
    if (res.code === 200) {
      ElMessage.success('更新成功')
      fetchUserInfo()
    } else {
      ElMessage.error(res.message)
    }
  } catch (error) {
    console.error(error)
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const res = await changePassword(passwordForm)
        if (res.code === 200) {
          ElMessage.success('密码修改成功')
          passwordForm.old_password = ''
          passwordForm.new_password = ''
          passwordForm.confirm_password = ''
        } else {
          ElMessage.error(res.message)
        }
      } catch (error) {
        console.error(error)
      }
    }
  })
}

// 头像上传前校验
const beforeAvatarUpload = (rawFile) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(rawFile.type)) {
    ElMessage.error('头像图片只能是 JPG/PNG/GIF 格式!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('头像图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 自定义上传头像
const handleAvatarUpload = async (options) => {
  const formData = new FormData()
  formData.append('file', options.file)
  
  try {
    const res = await uploadAvatar(formData)
    if (res.code === 200) {
      ElMessage.success('头像上传成功')
      userInfo.value.avatar = res.data.avatar_url
      // 同步更新全局用户信息，确保导航栏头像即时刷新
      store.commit('SET_USER_INFO', {
        ...(store.state.userInfo || {}),
        avatar: res.data.avatar_url
      })
    } else {
      ElMessage.error(res.message)
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('上传失败')
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: #f0f7ff;
  padding-top: 70px;
}

.page-shell {
  max-width: 100%;
  margin: 0;
  padding: 24px 40px;
}

.profile-hero {
  margin-bottom: 20px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.profile-hero h2 {
  font-size: 24px;
  margin: 8px 0 4px 0;
  color: #303133;
}

.profile-hero .section-sub {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.profile-hero .floating-badge {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1976d2;
  font-size: 12px;
  border-radius: 12px;
  margin-bottom: 8px;
}

.box-card {
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  color: #1976d2;
}

.user-info-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 0;
}

.avatar-uploader .avatar {
  width: 100px;
  height: 100px;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>