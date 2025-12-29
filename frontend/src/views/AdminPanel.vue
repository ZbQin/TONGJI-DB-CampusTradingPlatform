<template>
  <div class="admin-panel">
    <div class="admin-header">
      <h1>管理员后台</h1>
      <div class="admin-info">
        <span>欢迎，{{ adminInfo.username }}</span>
        <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="admin-tabs">
      <!-- 举报管理 -->
      <el-tab-pane label="举报管理" name="reports">
        <div class="filter-bar">
          <el-select v-model="reportFilter.status" placeholder="状态" clearable style="width: 120px" @change="loadReports">
            <el-option label="待处理" :value="0" />
            <el-option label="已处理" :value="1" />
            <el-option label="已驳回" :value="2" />
          </el-select>
          <el-select v-model="reportFilter.target_type" placeholder="类型" clearable style="width: 120px; margin-left: 10px" @change="loadReports">
            <el-option label="商品举报" :value="0" />
            <el-option label="用户举报" :value="1" />
          </el-select>
          <el-button type="primary" @click="loadReports" style="margin-left: 10px">刷新</el-button>
        </div>

        <el-table :data="reportList" style="width: 100%; margin-top: 20px" v-loading="reportLoading">
          <el-table-column prop="report_id" label="ID" width="60" />
          <el-table-column label="举报类型" width="100">
            <template #default="{ row }">
              <el-tag :type="row.target_type === 0 ? 'success' : 'warning'">
                {{ row.target_type === 0 ? '商品' : '用户' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="reporter_nickname" label="举报人" width="120" />
          <el-table-column prop="reported_nickname" label="被举报人" width="120" />
          <el-table-column prop="reason" label="举报原因" show-overflow-tooltip />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 0 ? 'info' : row.status === 1 ? 'success' : 'danger'">
                {{ row.status === 0 ? '待处理' : row.status === 1 ? '已处理' : '已驳回' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="举报时间" width="160" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button v-if="row.status === 0" type="success" size="small" @click="handleReportAction(row, 1)">通过</el-button>
              <el-button v-if="row.status === 0" type="warning" size="small" @click="handleReportAction(row, 2)">驳回</el-button>
              <el-button type="danger" size="small" @click="handleDeleteReport(row.report_id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          :current-page="reportPage"
          :page-size="20"
          :total="reportTotal"
          layout="total, prev, pager, next"
          @current-change="loadReports"
          style="margin-top: 20px; justify-content: center"
        />
      </el-tab-pane>

      <!-- 用户封禁 -->
      <el-tab-pane label="用户管理" name="users">
        <div class="user-action-card">
          <h3>封禁/解封用户</h3>
          <el-form :model="userForm" label-width="100px" style="max-width: 500px">
            <el-form-item label="用户ID">
              <el-input v-model.number="userForm.user_id" placeholder="请输入用户ID" />
            </el-form-item>
            <el-form-item label="操作类型">
              <el-radio-group v-model="userForm.action">
                <el-radio value="ban">封禁</el-radio>
                <el-radio value="unban">解封</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item v-if="userForm.action === 'ban'" label="封禁原因">
              <el-input v-model="userForm.reason" type="textarea" placeholder="请输入封禁原因" :rows="3" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleUserAction" :loading="userActionLoading">提交</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

      <!-- 发送通知 -->
      <el-tab-pane label="发送通知" name="notification">
        <div class="notification-card">
          <h3>向用户发送通知</h3>
          <el-form :model="notifyForm" label-width="100px" style="max-width: 600px">
            <el-form-item label="用户ID">
              <el-input v-model.number="notifyForm.user_id" placeholder="请输入用户ID" />
            </el-form-item>
            <el-form-item label="通知类型">
              <el-select v-model="notifyForm.type" placeholder="请选择">
                <el-option label="系统通知" :value="0" />
                <el-option label="账户通知" :value="1" />
                <el-option label="交易通知" :value="2" />
                <el-option label="其他" :value="3" />
              </el-select>
            </el-form-item>
            <el-form-item label="通知标题">
              <el-input v-model="notifyForm.title" placeholder="请输入标题" />
            </el-form-item>
            <el-form-item label="通知内容">
              <el-input v-model="notifyForm.content" type="textarea" placeholder="请输入通知内容" :rows="5" />
            </el-form-item>
            <el-form-item label="关联ID">
              <el-input v-model.number="notifyForm.related_id" placeholder="可选，关联对象ID" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSendNotification" :loading="notifyLoading">发送通知</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getReportList, handleReport, deleteReport, banUser, unbanUser, sendNotification } from '@/api/admin'

export default {
  name: 'AdminPanel',
  setup() {
    const router = useRouter()
    const activeTab = ref('reports')
    const adminInfo = reactive(JSON.parse(localStorage.getItem('adminInfo') || '{}'))

    // 举报管理
    const reportList = ref([])
    const reportLoading = ref(false)
    const reportPage = ref(1)
    const reportTotal = ref(0)
    const reportFilter = reactive({
      status: null,
      target_type: null
    })

    const loadReports = async (page = 1) => {
      reportPage.value = page
      reportLoading.value = true
      try {
        const params = {
          page: reportPage.value,
          page_size: 20
        }
        if (reportFilter.status !== null && reportFilter.status !== '') {
          params.status = reportFilter.status
        }
        if (reportFilter.target_type !== null && reportFilter.target_type !== '') {
          params.target_type = reportFilter.target_type
        }

        const res = await getReportList(params)
        if (res.code === 200) {
          reportList.value = res.data.list
          reportTotal.value = res.data.total
        }
      } catch (e) {
        console.error(e)
      } finally {
        reportLoading.value = false
      }
    }

    const handleReportAction = async (report, status) => {
      try {
        const actionText = status === 1 ? '通过' : '驳回'
        const { value: handleResult } = await ElMessageBox.prompt(
          `请输入处理说明（${actionText}举报）`,
          '处理举报',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputPlaceholder: '处理说明',
            inputValue: status === 1 ? '举报属实，已处理' : '举报不成立'
          }
        )

        const res = await handleReport(report.report_id, {
          status,
          handle_result: handleResult || ''
        })

        if (res.code === 200) {
          ElMessage.success(`${actionText}成功`)
          loadReports()
        }
      } catch (e) {
        if (e !== 'cancel') {
          console.error(e)
        }
      }
    }

    const handleDeleteReport = async (reportId) => {
      try {
        await ElMessageBox.confirm('确定要删除这条举报吗？', '提示', {
          type: 'warning'
        })

        const res = await deleteReport(reportId)
        if (res.code === 200) {
          ElMessage.success('删除成功')
          loadReports()
        }
      } catch (e) {
        if (e !== 'cancel') {
          console.error(e)
        }
      }
    }

    // 用户管理
    const userForm = reactive({
      user_id: null,
      action: 'ban',
      reason: ''
    })
    const userActionLoading = ref(false)

    const handleUserAction = async () => {
      if (!userForm.user_id) {
        ElMessage.warning('请输入用户ID')
        return
      }

      if (userForm.action === 'ban' && !userForm.reason) {
        ElMessage.warning('请输入封禁原因')
        return
      }

      userActionLoading.value = true
      try {
        let res
        if (userForm.action === 'ban') {
          res = await banUser(userForm.user_id, { reason: userForm.reason })
        } else {
          res = await unbanUser(userForm.user_id)
        }

        if (res.code === 200) {
          ElMessage.success(userForm.action === 'ban' ? '封禁成功' : '解封成功')
          userForm.user_id = null
          userForm.reason = ''
        }
      } catch (e) {
        console.error(e)
      } finally {
        userActionLoading.value = false
      }
    }

    // 发送通知
    const notifyForm = reactive({
      user_id: null,
      type: 0,
      title: '',
      content: '',
      related_id: null
    })
    const notifyLoading = ref(false)

    const handleSendNotification = async () => {
      if (!notifyForm.user_id || !notifyForm.title || !notifyForm.content) {
        ElMessage.warning('请填写完整信息')
        return
      }

      notifyLoading.value = true
      try {
        const res = await sendNotification(notifyForm)
        if (res.code === 200) {
          ElMessage.success('通知发送成功')
          notifyForm.user_id = null
          notifyForm.title = ''
          notifyForm.content = ''
          notifyForm.related_id = null
        }
      } catch (e) {
        console.error(e)
      } finally {
        notifyLoading.value = false
      }
    }

    // 退出登录
    const handleLogout = () => {
      localStorage.removeItem('adminToken')
      localStorage.removeItem('adminInfo')
      ElMessage.success('已退出登录')
      router.push('/admin-login')
    }

    onMounted(() => {
      if (!localStorage.getItem('adminToken')) {
        ElMessage.warning('请先登录')
        router.push('/admin-login')
        return
      }
      loadReports()
    })

    return {
      activeTab,
      adminInfo,
      reportList,
      reportLoading,
      reportPage,
      reportTotal,
      reportFilter,
      loadReports,
      handleReportAction,
      handleDeleteReport,
      userForm,
      userActionLoading,
      handleUserAction,
      notifyForm,
      notifyLoading,
      handleSendNotification,
      handleLogout
    }
  }
}
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 20px 30px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.admin-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.admin-info span {
  color: #666;
  font-size: 14px;
}

.admin-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  min-height: calc(100vh - 160px);
}

.filter-bar {
  display: flex;
  align-items: center;
}

.user-action-card,
.notification-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.user-action-card h3,
.notification-card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

:deep(.el-tabs__content) {
  padding: 20px 0;
}

:deep(.el-pagination) {
  display: flex;
}
</style>
