<template>
  <el-dialog
    v-model="dialogVisible"
    title="评价用户"
    width="500px"
    @close="handleClose"
    class="review-dialog"
  >
    <el-form :model="reviewForm" :rules="rules" ref="formRef" label-width="80px">
      <el-form-item label="评分" prop="rating">
        <el-rate 
          v-model="reviewForm.rating" 
          :texts="['极差', '失望', '一般', '满意', '惊喜']"
          show-text
          :colors="['#F56C6C', '#E6A23C', '#409EFF']"
        />
      </el-form-item>
      
      <el-form-item label="评价内容" prop="comment">
        <el-input
          v-model="reviewForm.comment"
          type="textarea"
          :rows="5"
          placeholder="请输入您的评价内容..."
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          提交评价
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { ref, reactive, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { createReview } from '@/api/review'
import { getProducts } from '@/api/product'

export default {
  name: 'ReviewModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    revieweeId: {
      type: Number,
      required: true
    },
    revieweeName: {
      type: String,
      default: ''
    }
  },
  emits: ['close', 'success'],
  setup(props, { emit }) {
    const dialogVisible = ref(props.visible)
    const formRef = ref(null)
    const submitting = ref(false)
    const products = ref([])
    
    const reviewForm = reactive({
      rating: 5,
      comment: ''
    })
    
    const rules = {
      rating: [
        { required: true, message: '请选择评分', trigger: 'change' }
      ],
      comment: [
        { required: true, message: '请输入评价内容', trigger: 'blur' },
        { min: 5, max: 500, message: '评价内容长度在5到500个字符', trigger: 'blur' }
      ]
    }
    
    watch(() => props.visible, (val) => {
      dialogVisible.value = val
    })
    
    const fetchProducts = async () => {
      try {
        const res = await getProducts({ pageNum: 1, pageSize: 100 })
        products.value = res.data.products || []
      } catch (error) {
        console.error('获取商品列表失败:', error)
      }
    }
    
    const handleClose = () => {
      emit('close')
    }
    
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            submitting.value = true
            await createReview({
              reviewee_id: props.revieweeId,
              rating: reviewForm.rating,
              content: reviewForm.comment  // 后端期望的字段名是content
            })
            
            ElMessage.success('评价成功')
            emit('success')
            handleClose()
          } catch (error) {
            ElMessage.error(error.response?.data?.message || '评价失败')
          } finally {
            submitting.value = false
          }
        }
      })
    }
    
    onMounted(() => {
      fetchProducts()
    })
    
    return {
      dialogVisible,
      formRef,
      reviewForm,
      rules,
      submitting,
      products,
      handleClose,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.review-dialog :deep(.el-dialog) {
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(227, 242, 253, 0.95));
  backdrop-filter: blur(10px);
}

.review-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
  border-radius: 16px 16px 0 0;
  padding: 20px;
}

.review-dialog :deep(.el-dialog__title) {
  color: white;
  font-weight: bold;
}

.review-dialog :deep(.el-dialog__close) {
  color: white;
}

.review-dialog :deep(.el-form-item__label) {
  color: #1976d2;
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
