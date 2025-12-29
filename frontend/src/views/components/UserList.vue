<template>
  <el-table :data="list" v-loading="loading" style="width: 100%">
    <el-table-column label="头像" width="80">
      <template #default="{ row }">
        <el-avatar :size="40" :src="row.avatar" />
      </template>
    </el-table-column>
    <el-table-column prop="nickname" label="昵称" min-width="160" />
    <el-table-column prop="phone" label="电话" min-width="140" />
    <el-table-column prop="created_at" label="时间" width="180" />
    <el-table-column label="操作" width="140" fixed="right">
      <template #default="{ row }">
        <el-button
          v-if="showAction(row)"
          size="small"
          type="primary"
          plain
          @click="$emit('action', row.user_id)"
        >{{ actionText }}</el-button>
        <span v-else style="color:#67c23a">已关注</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
defineProps({
  list: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  actionText: { type: String, default: '操作' },
  showAction: { type: Function, default: () => true }
})
</script>

<style scoped>
</style>
