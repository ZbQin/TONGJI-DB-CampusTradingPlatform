<template>
  <div class="wanted-publish-container">
    <NavBar />
    <div class="page-shell">
      <div class="hero-shell publish-hero">
        <div>
          <div class="floating-badge">发布求购</div>
          <h2>描述需求，同学更快响应</h2>
          <p class="section-sub">填写标题、分类和期望价格，帮助卖家精准匹配</p>
        </div>
        <el-button class="ghost-button" @click="goHome">返回首页</el-button>
      </div>

      <el-card class="soft-card glass">
        <template #header>
          <div class="card-header">
            <span>求购信息</span>
          </div>
        </template>

        <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" class="form-body">
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" placeholder="如：求购二手iPad" />
          </el-form-item>
          <el-form-item label="分类" prop="category_id">
            <el-select v-model="form.category_id" placeholder="请选择分类">
              <el-option v-for="c in categories" :key="c.category_id" :label="c.name" :value="c.category_id" />
            </el-select>
          </el-form-item>
          <el-form-item label="期望价格" prop="expected_price">
            <el-input-number v-model="form.expected_price" :min="0" :step="10" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input type="textarea" v-model="form.description" :rows="4" placeholder="描述需求、成色期望等" />
          </el-form-item>
          <el-form-item class="actions-row">
            <el-button type="primary" :loading="loading" @click="submit">发布</el-button>
            <el-button class="ghost-button" @click="goHome">返回首页</el-button>
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
import NavBar from '@/components/NavBar.vue'
import { publishWanted } from '@/api/wanted'
import { getCategoryList } from '@/api/category'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const categories = ref([])
const form = reactive({
  title: '',
  category_id: null,
  expected_price: 0,
  description: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  expected_price: [{ required: true, message: '请输入期望价格', trigger: 'blur' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }]
}

const loadCategories = async () => {
  const res = await getCategoryList()
  if (res.code === 200) categories.value = res.data
}

const goHome = () => {
  router.push('/')
}

const submit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await publishWanted({ ...form })
      if (res.code === 200) {
        ElMessage.success('发布成功')
        router.push('/wanted')
      } else {
        ElMessage.error(res.message || '发布失败')
      }
    } catch (error) {
      ElMessage.error('发布失败')
    } finally {
      loading.value = false
    }
  })
}

onMounted(loadCategories)
</script>

<style scoped>
.wanted-publish-container {
  min-height: 100vh;
  background: #f0f7ff;
  padding-top: 70px;
}

.page-shell {
  max-width: 100%;
  margin: 0;
  padding: 24px 40px;
}

.soft-card {
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
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

.form-body {
  padding: 8px 0;
}

.form-body :deep(.el-form-item) {
  margin-bottom: 18px;
}

.form-body :deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

.actions-row {
  margin-top: 8px;
}
</style>
