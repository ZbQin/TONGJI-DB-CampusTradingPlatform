<template>
  <div class="product-edit-container">
    <NavBar />
    <div class="page-shell">
      <div class="hero-shell publish-hero">
        <div>
          <div class="floating-badge">编辑商品</div>
          <h2>更新你的商品信息</h2>
          <p class="section-sub">调整价格、描述或图片，让买家获取最新信息</p>
        </div>
        <el-button class="ghost-button" @click="goBack">返回</el-button>
      </div>

      <el-card class="soft-card glass">
        <template #header>
          <div class="card-header">商品信息</div>
        </template>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          class="form-body"
        >
          <el-form-item label="商品标题" prop="title">
            <el-input v-model="form.title" placeholder="请输入商品标题" />
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
              placeholder="描述成色、配件、交易方式等"
            />
          </el-form-item>

          <el-form-item label="已上传图片">
            <div v-if="existingImages.length" class="image-list">
              <div v-for="(img, idx) in existingImages" :key="img" class="image-thumb">
                <img :src="img" alt="product" />
                <el-button type="danger" text size="small" @click="removeExisting(idx)">移除</el-button>
              </div>
            </div>
            <div v-else class="no-image">暂无图片</div>
          </el-form-item>

          <el-form-item label="新增图片">
            <el-upload
              class="image-uploader"
              action="#"
              list-type="picture-card"
              :show-file-list="false"
              :auto-upload="false"
              multiple
              :on-change="handleFileChange"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
            <div v-if="newImagePreviews.length" class="image-list">
              <div v-for="(img, idx) in newImagePreviews" :key="img" class="image-thumb">
                <img :src="img" alt="new" />
                <el-button type="primary" text size="small" @click="removeNew(idx)">移除</el-button>
              </div>
            </div>
            <div class="upload-tip">第一张图将作为封面</div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" :loading="loading" @click="submit">保存修改</el-button>
            <el-button @click="goBack">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import { getCategoryList } from '@/api/category'
import { getProductDetail, updateProduct, uploadProductImage } from '@/api/product'

const route = useRoute()
const router = useRouter()
const productId = route.params.id

const formRef = ref(null)
const loading = ref(false)
const categories = ref([])
const existingImages = ref([])
const newImageFiles = ref([])
const newImagePreviews = ref([])

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

const loadCategories = async () => {
  const res = await getCategoryList()
  if (res.code === 200) categories.value = res.data
}

const loadDetail = async () => {
  const res = await getProductDetail(productId)
  if (res.code === 200 && res.data) {
    const data = res.data
    form.title = data.title
    form.price = data.price
    form.category_id = data.category_id
    form.description = data.description
    existingImages.value = (data.images || []).map((img) => img.image_url || img)
  }
}

const goBack = () => router.back()

const handleFileChange = (file) => {
  newImageFiles.value.push(file.raw)
  if (file.raw) {
    newImagePreviews.value.push(URL.createObjectURL(file.raw))
  }
}

const removeExisting = (idx) => {
  existingImages.value.splice(idx, 1)
}

const removeNew = (idx) => {
  newImageFiles.value.splice(idx, 1)
  newImagePreviews.value.splice(idx, 1)
}

const submit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const uploaded = []
      for (const file of newImageFiles.value) {
        const formData = new FormData()
        formData.append('file', file)
        const r = await uploadProductImage(formData)
        if (r.code === 200 && r.data?.image_url) {
          uploaded.push(r.data.image_url)
        }
      }

      const payloadImages = [...existingImages.value, ...uploaded]
      const payload = {
        product_id: Number(productId),
        title: form.title,
        price: form.price,
        category_id: form.category_id,
        description: form.description,
        images: payloadImages
      }

      const res = await updateProduct(payload)
      if (res.code === 200) {
        ElMessage.success('保存成功')
        router.push('/my-items')
      } else {
        ElMessage.error(res.message || '保存失败')
      }
    } catch (error) {
      ElMessage.error('保存失败')
    } finally {
      loading.value = false
    }
  })
}

onMounted(async () => {
  await Promise.all([loadCategories(), loadDetail()])
})
</script>

<style scoped>
.product-edit-container {
  min-height: 100vh;
  background: var(--bg-page);
}
.page-shell {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px 30px;
}
.card-header {
  font-size: 18px;
  font-weight: 600;
}
.form-body {
  padding-top: 8px;
}
.unit {
  margin-left: 8px;
  color: #909399;
}
.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.image-thumb {
  width: 120px;
  height: 120px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background: #f6f7f9;
  border: 1px solid #ebeef5;
}
.image-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.image-thumb .el-button {
  position: absolute;
  bottom: 4px;
  left: 4px;
}
.no-image {
  color: #909399;
  font-size: 13px;
}
.upload-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 6px;
}
</style>
