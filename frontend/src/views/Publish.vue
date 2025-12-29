<template>
  <div class="publish-container">
    <NavBar />
    <div class="page-shell">
      <div class="hero-shell publish-hero">
        <div>
          <div class="floating-badge">3步完成发布</div>
          <h2>把你的好物带给下一位同学</h2>
          <p class="section-sub">上传图片、填写描述，10 秒内发布成功</p>
        </div>
        <el-button class="ghost-button" @click="goHome">返回首页</el-button>
      </div>

      <el-card class="publish-card soft-card glass">
        <template #header>
          <div class="card-header">
            <span>发布商品</span>
          </div>
        </template>

        <el-form 
          ref="publishFormRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          class="publish-form"
        >
          <el-form-item label="商品标题" prop="title">
            <el-input v-model="form.title" placeholder="请输入商品标题（如：99新 iPad Air 5）" />
          </el-form-item>
          
          <el-form-item label="商品价格" prop="price">
            <el-input-number v-model="form.price" :precision="2" :step="1" :min="0" />
            <span class="unit">元</span>
          </el-form-item>
          
          <el-form-item label="商品分类" prop="category_id">
            <el-select v-model="form.category_id" placeholder="请选择分类">
              <el-option 
                v-for="cat in categories" 
                :key="cat.category_id" 
                :label="cat.name" 
                :value="cat.category_id" 
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="商品描述" prop="description">
            <el-input 
              v-model="form.description" 
              type="textarea" 
              :rows="4" 
              placeholder="描述一下商品的成色、入手渠道、转手原因等..." 
            />
          </el-form-item>
          
          <el-form-item label="商品图片">
            <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :auto-upload="false"
              :on-change="handleFileChange"
            >
              <img v-if="imageUrl" :src="imageUrl" class="avatar" />
              <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">支持 jpg/png 格式，大小不超过 2MB</div>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitForm" :loading="loading">立即发布</el-button>
            <el-button @click="$router.back()">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import { publishProduct, uploadProductImage } from '@/api/product'
import { getCategoryList } from '@/api/category'

const router = useRouter()
const publishFormRef = ref(null)
const loading = ref(false)
const uploadedImages = ref([])
const imageFiles = ref([])
const categories = ref([])

const form = reactive({
  title: '',
  price: 0,
  category_id: null,
  description: ''
})

const rules = {
  title: [{ required: true, message: '请输入商品标题', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  description: [{ required: true, message: '请输入商品描述', trigger: 'blur' }]
}

// 加载分类列表
const loadCategories = async () => {
  try {
    const res = await getCategoryList()
    if (res.code === 200) {
      categories.value = res.data
    }
  } catch (error) {
    ElMessage.error('加载分类列表失败')
  }
}

const handleFileChange = (file) => {
  imageFiles.value.push(file.raw)
}

const goHome = () => {
  router.replace('/')
}

const submitForm = async () => {
  if (!publishFormRef.value) return
  
  await publishFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 上传所有图片
        const imageUrls = []
        for (const file of imageFiles.value) {
          const formData = new FormData()
          formData.append('file', file)
          const imgRes = await uploadProductImage(formData)
          if (imgRes.code === 200) {
            imageUrls.push(imgRes.data.image_url)
          }
        }
        
        // 发布商品
        const productData = { 
          ...form, 
          images: imageUrls
        }
        const res = await publishProduct(productData)
        
        if (res.code === 200) {
          ElMessage.success('发布成功')
          router.push('/')
        } else {
          ElMessage.error(res.message || '发布失败')
        }
      } catch (error) {
        console.error(error)
        ElMessage.error('发布失败')
      } finally {
        loading.value = false
      }
    }
  })
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.publish-container {
  min-height: 100vh;
  background: var(--bg-page);
}

.page-shell {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}

.publish-card {
  border-radius: 14px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.publish-hero {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.unit {
  margin-left: 10px;
  color: #606266;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 148px;
  height: 148px;
  text-align: center;
  line-height: 148px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
}

.avatar {
  width: 148px;
  height: 148px;
  display: block;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>