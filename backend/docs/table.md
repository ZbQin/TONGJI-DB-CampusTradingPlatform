# 校园交易平台数据库设计

## 1. 用户相关表

### 1.1 用户表 (user)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| user_id | BIGINT | 用户ID | 主键，自增 |
| username | VARCHAR(50) | 用户名 | 唯一，非空 |
| password | VARCHAR(255) | 密码（加密） | 非空 |
| nickname | VARCHAR(50) | 昵称| 非空，默认与用户名相同 |
| avatar | VARCHAR(255) | 头像URL | |
| campus | VARCHAR(100) | 所在校区 | |
| dormitory | VARCHAR(100) | 宿舍楼 | |
| bio | TEXT | 个人简介 | |
| credit_score | INT | 信用积分 | 默认5 |
| status | TINYINT | 账户状态 | 0-正常 1-封禁 |
| created_at | DATETIME | 注册时间 | 默认当前时间 |
| updated_at | DATETIME | 更新时间 | 默认当前时间 |

## 2. 商品相关表

### 2.1 商品分类表 (category)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| category_id | INT | 分类ID | 主键，自增 |
| name | VARCHAR(50) | 分类名称 | 唯一，非空 |
| sort_order | INT | 排序 | 默认0 |
| status | TINYINT | 状态 | 0-禁用 1-启用，默认1 |
| created_at | DATETIME | 创建时间 | 默认当前时间 |
| updated_at | DATETIME | 更新时间 | 默认当前时间 |

### 2.2 商品表 (product)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| product_id | BIGINT | 商品ID | 主键，自增 |
| user_id | BIGINT | 卖家ID | 外键，关联user |
| title | VARCHAR(200) | 商品标题 | 非空 |
| description | TEXT | 商品描述 | 非空 |
| category_id | INT | 商品分类 | 非空，外键，关联category |
| price | DECIMAL(10,2) | 价格 | 非空 |
| favorite_count | INT | 收藏次数 | 默认0 |
| status | TINYINT | 商品状态 | 0-出售中 1-已售出 2-已下架 |
| is_featured | TINYINT | 是否精选 | 0-否 1-是 |
| audit_status | TINYINT | 审核状态 | 0-待审核 1-通过 2-拒绝 |
| created_at | DATETIME | 发布时间 | 默认当前时间 |
| updated_at | DATETIME | 更新时间 | 默认当前时间 |

### 2.3 商品图片表 (product_image)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| image_id | BIGINT | 图片ID | 主键，自增 |
| product_id | BIGINT | 商品ID | 外键，关联products |
| image_url | VARCHAR(255) | 图片URL | 非空 |
| is_cover | TINYINT | 是否封面 | 0-否 1-是 |
| sort_order | INT | 排序 | 默认0 |
| created_at | DATETIME | 上传时间 | 默认当前时间 |



## 3. 交互功能表

### 3.1 收藏表 (favorites)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| favorite_id | BIGINT | 收藏ID | 主键，自增 |
| user_id | BIGINT | 用户ID | 外键，关联users |
| product_id | BIGINT | 商品ID | 外键，关联products |
| created_at | DATETIME | 收藏时间 | 默认当前时间 |

索引：user_id, product_id 联合唯一索引

### 3.2 关注表 (follows)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| follow_id | BIGINT | 关注ID | 主键，自增 |
| follower_id | BIGINT | 关注者ID | 外键，关联users |
| followee_id | BIGINT | 被关注者ID | 外键，关联users |
| created_at | DATETIME | 关注时间 | 默认当前时间 |

索引：follower_id, followee_id 联合唯一索引

### 3.3 求购表 (wanted)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| wanted_id | BIGINT | 求购ID | 主键，自增 |
| user_id | BIGINT | 用户ID | 外键，关联user |
| category_id | INT | 分类ID | 外键，关联category |
| title | VARCHAR(200) | 求购标题 | 非空 |
| description | TEXT | 详细描述 | 非空 |
| expected_price | DECIMAL(10,2) | 期望价格 | 默认0 |
| status | INT | 状态 | 0-进行中 1-已完成 2-已取消，默认0 |
| created_at | DATETIME | 发布时间 | 默认当前时间 |
| updated_at | DATETIME | 更新时间 | 默认当前时间 |

索引：user_id, category_id, status, created_at


## 4. 沟通交流表

### 4.1 聊天会话表 (chat_session)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| session_id | BIGINT | 会话ID | 主键，自增 |
| product_id | BIGINT | 商品ID | 外键，关联products |
| buyer_id | BIGINT | 买家ID | 外键，关联users |
| seller_id | BIGINT | 卖家ID | 外键，关联users |
| last_message | TEXT | 最后一条消息 | |
| last_message_time | DATETIME | 最后消息时间 | |
| unread_count_buyer | INT | 买家未读数 | 默认0 |
| unread_count_seller | INT | 卖家未读数 | 默认0 |
| created_at | DATETIME | 创建时间 | 默认当前时间 |
| updated_at | DATETIME | 更新时间 | 默认当前时间 |

### 4.2 聊天消息表 (chat_message)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| message_id | BIGINT | 消息ID | 主键，自增 |
| session_id | BIGINT | 会话ID | 外键，关联chat_sessions |
| sender_id | BIGINT | 发送者ID | 外键，关联users |
| receiver_id | BIGINT | 接收者ID | 外键，关联users |
| message_type | TINYINT | 消息类型 | 0-文本 1-图片 |
| content | TEXT | 消息内容 | 非空 |
| is_read | TINYINT | 是否已读 | 0-未读 1-已读 |
| created_at | DATETIME | 发送时间 | 默认当前时间 |

## 5. 交易与评价

### 5.1 评价表 (reviews)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| review_id | BIGINT | 评价ID | 主键，自增 |
| reviewer_id | BIGINT | 评价者ID | 外键，关联users |
| reviewee_id | BIGINT | 被评价者ID | 外键，关联users |
| product_id | BIGINT | 关联商品ID | 外键，关联product，可为NULL |
| rating | TINYINT | 评分 | 1-5分 |
| content | TEXT | 评价内容 | |
| created_at | DATETIME | 评价时间 | 默认当前时间 |

索引：reviewer_id, reviewee_id, product_id, created_at

## 6. 安全与管理表

### 6.1 举报表 (reports)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| report_id | BIGINT | 举报ID | 主键，自增 |
| reporter_id | BIGINT | 举报者ID | 外键，关联users |
| reported_id | BIGINT | 被举报者ID | 外键，关联users |
| target_type | TINYINT | 举报对象类型 | 0-商品 1-用户 |
| target_id | BIGINT | 举报对象ID | |
| reason | VARCHAR(255) | 举报原因 | 非空 |
| description | TEXT | 详细描述 | |
| status | TINYINT | 处理状态 | 0-待处理 1-已处理 2-已驳回 |
| handler_id | BIGINT | 处理人ID | 外键，关联admins |
| handle_result | TEXT | 处理结果 | |
| handle_time | DATETIME | 处理时间 | |
| created_at | DATETIME | 举报时间 | 默认当前时间 |

### 6.2 管理员表 (admins)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| admin_id | BIGINT | 管理员ID | 主键，自增 |
| username | VARCHAR(50) | 用户名 | 唯一，非空 |
| password_hash | VARCHAR(255) | 密码（加密） | 非空 |
| role | TINYINT | 角色 | 0-超级管理员 1-普通管理员，默认1 |
| status | TINYINT | 状态 | 0-禁用 1-正常，默认1 |
| last_login_time | DATETIME | 最后登录时间 | |
| created_at | DATETIME | 创建时间 | 默认当前时间 |
| updated_at | DATETIME | 更新时间 | 默认当前时间 |

### 6.3 系统通知表 (notification)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| notification_id | BIGINT | 通知ID | 主键，自增 |
| user_id | BIGINT | 接收用户ID | 外键，关联users |
| type | TINYINT | 通知类型 | 0-系统 1-账户操作 2-交易 3-评价，默认0 |
| title | VARCHAR(200) | 通知标题 | 非空 |
| content | TEXT | 通知内容 | 非空 |
| related_id | BIGINT | 关联对象ID | 可为NULL，如商品ID/举报ID等 |
| is_read | TINYINT | 是否已读 | 0-未读 1-已读，默认0 |
| created_at | DATETIME | 创建时间 | 默认当前时间 |

索引：user_id, is_read, type, created_at

## 索引建议

### 关键索引

1. **users表**
   - idx_phone (phone)
   - idx_email (email)
   - idx_status (status)

2. **products表**
   - idx_user_id (user_id)
   - idx_category_id (category_id)
   - idx_status (status)
   - idx_created_at (created_at)
   - idx_price (price)

3. **orders表**
   - idx_order_no (order_no)
   - idx_buyer_id (buyer_id)
   - idx_seller_id (seller_id)
   - idx_status (status)
   - idx_created_at (created_at)

4. **chat_messages表**
   - idx_session_id (session_id)
   - idx_created_at (created_at)

5. **favorites表**
   - unique_user_product (user_id, product_id)

## 外键约束建议

建议在生产环境中根据实际情况选择性使用外键约束，以平衡数据完整性和性能。可以通过应用层逻辑来保证数据一致性。

## 表分区建议

对于大数据量的表，建议进行分区：
- **chat_messages**: 按月份分区
- **operation_logs**: 按月份分区
- **transaction_statistics**: 按年份分区
