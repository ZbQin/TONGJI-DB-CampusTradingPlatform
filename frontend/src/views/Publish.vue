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
              class="image-uploader"
              action="#"
              list-type="picture-card"
              :auto-upload="false"
              :on-change="handleFileChange"
              :on-remove="handleRemove"
              :file-list="fileList"
              multiple
              accept="image/*"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">支持 jpg/png 格式，大小不超过 2MB，第一张图将作为封面</div>
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
const imageFiles = ref([])
const fileList = ref([])
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
  if (file.raw) {
    imageFiles.value.push(file.raw)
  }
}

const handleRemove = (file) => {
  const index = fileList.value.findIndex(f => f.uid === file.uid)
  if (index > -1) {
    imageFiles.value.splice(index, 1)
  }
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
  background: #f0f7ff;
  padding-top: 70px;
}

.page-shell {
  max-width: 100%;
  margin: 0;
  padding: 24px 40px;
}

.publish-card {
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
}

.card-header {
  font-size: 20px;
  font-weight: bold;
  color: #1976d2;
}

.publish-hero {
  margin-bottom: 20px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.publish-hero h2 {
  font-size: 24px;
  margin: 8px 0 4px 0;
  color: #303133;
}

.publish-hero .section-sub {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.publish-form {
  padding: 8px 0;
}

.publish-form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.publish-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

.unit {
  margin-left: 10px;
  color: #909399;
}

.image-uploader :deep(.el-upload--picture-card) {
  width: 120px;
  height: 120px;
  line-height: 120px;
  border-radius: 8px;
}

.image-uploader :deep(.el-upload-list__item) {
  width: 120px;
  height: 120px;
  border-radius: 8px;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}
</style>