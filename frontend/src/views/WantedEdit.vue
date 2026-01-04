<template>
  <div class="wanted-edit-container">
    <NavBar />
    <div class="page-shell">
      <div class="hero-shell publish-hero">
        <div>
          <div class="floating-badge">编辑求购</div>
          <h2>更新你的求购需求</h2>
          <p class="section-sub">调整标题、分类或期望价格，便于卖家响应</p>
        </div>
        <el-button class="ghost-button" @click="goBack">返回</el-button>
      </div>

      <el-card class="soft-card glass">
        <template #header>
          <div class="card-header">求购信息</div>
        </template>

        <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" class="form-body">
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" placeholder="请输入求购标题" />
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
            <el-input type="textarea" v-model="form.description" :rows="4" placeholder="描述你的需求" />
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
import NavBar from '@/components/NavBar.vue'
import { getCategoryList } from '@/api/category'
import { getWantedDetail, updateWanted } from '@/api/wanted'

const route = useRoute()
const router = useRouter()
const wantedId = route.params.id

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

const loadDetail = async () => {
  const res = await getWantedDetail(wantedId)
  if (res.code === 200 && res.data) {
    const d = res.data
    form.title = d.title
    form.category_id = d.category_id
    form.expected_price = d.expected_price
    form.description = d.description
  }
}

const goBack = () => router.back()

const submit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const payload = {
        wanted_id: Number(wantedId),
        title: form.title,
        category_id: form.category_id,
        expected_price: form.expected_price,
        description: form.description
      }
      const res = await updateWanted(payload)
      if (res.code === 200) {
        ElMessage.success('保存成功')
        router.push('/wanted/my-list')
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
.wanted-edit-container {
  min-height: 100vh;
  background: var(--bg-page);
}
.page-shell {
  max-width: 840px;
  margin: 20px auto;
  padding: 0 20px 30px;
}
.card-header {
  font-size: 18px;
  font-weight: 600;
}
.publish-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  gap: 12px;
}
.form-body {
  padding-top: 8px;
}
</style>
