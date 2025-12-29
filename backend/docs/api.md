# 校园交易平台 API 文档

## 1. 用户认证模块

### 1.1 用户注册

**接口地址**: `/auth/register`

**请求方式**: `POST`

**是否需要登录**: 否

#### 请求示例

```json
{
  "username": "zhangsan",
  "password": "123456",
  "nickname": "张三"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "注册成功",
  "data": true
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "用户名已存在",
  "data": false
}
```

---

### 1.2 用户登录

**接口地址**: `/auth/login`

**请求方式**: `POST`

**是否需要登录**: 否

#### 请求示例

```json
{
  "username": "zhangsan",
  "password": "123456"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_info": {
      "user_id": 1001,
      "username": "zhangsan",
      "nickname": "张三",
      "avatar": "/static/uploads/avatars/avatar1.jpg"
    }
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "用户名或密码错误",
  "data": false
}
```

---

### 1.3 退出登录

**接口地址**: `/auth/logout`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

无

#### 响应示例

```json
{
  "code": 200,
  "message": "退出成功",
  "data": true
}
```

---

### 1.4 修改密码

**接口地址**: `/auth/change-password`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| old_password | string | 是 | 原密码 |
| new_password | string | 是 | 新密码，6-20个字符 |
| confirm_password | string | 是 | 确认新密码 |

#### 请求示例

```json
{
  "old_password": "123456",
  "new_password": "654321",
  "confirm_password": "654321"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": true
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "原密码错误",
  "data": false
}
```

---

### 1.5 获取当前用户信息

**接口地址**: `/auth/user-info`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

无

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1001,
    "username": "zhangsan",
    "nickname": "张三",
    "avatar": "https://example.com/avatar.png",
    "campus": "南校区",
    "dormitory": "1号楼",
    "bio": "这是我的个人简介",
    "credit_score": 100,
    "is_verified": 1,
    "status": 1,
    "created_at": "2025-11-20 10:30:00",
    "updated_at": "2025-11-20 10:30:00"
  }
}
```

---

### 1.6 更新用户信息

**接口地址**: `/auth/update-profile`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| nickname | string | 否 | 昵称 |
| avatar | string | 否 | 头像URL |
| campus | string | 否 | 所在校区 |
| dormitory | string | 否 | 宿舍楼 |
| bio | string | 否 | 个人简介 |

#### 请求示例

```json
{
  "nickname": "新昵称",
  "campus": "北校区",
  "dormitory": "2号楼",
  "bio": "更新后的个人简介"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "用户信息更新成功",
  "data": true
}
```

---

### 1.7 上传头像

**接口地址**: `/auth/upload-avatar`

**请求方式**: `POST`

**是否需要登录**: 是

**Content-Type**: `multipart/form-data`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | file | 是 | 图片文件 (jpg, png, gif) |

#### 响应示例

```json
{
  "code": 200,
  "message": "头像上传成功",
  "data": {
    "avatar_url": "/static/uploads/avatars/unique_filename.jpg"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "文件格式不支持",
  "data": false
}
```

---

## 2. 商品管理模块

### 2.1 发布商品

**接口地址**: `/product/publish`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| title | string | 是 | 商品标题，最多100字符 |
| description | string | 是 | 商品描述 |
| price | decimal | 是 | 价格，保留2位小数 |
| category | string | 是 | 分类（书籍教材/电子数码/生活用品/美妆护肤/运动器材/其他） |
| images | array | 否 | 图片URL数组，最多9张 |

#### 请求示例

```json
{
  "title": "二手高等数学教材",
  "description": "九成新，无笔记，配套习题册齐全",
  "price": 25.50,
  "category": "书籍教材",
  "images": [
    "/static/uploads/product/img1.jpg",
    "/static/uploads/product/img2.jpg"
  ]
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "发布成功",
  "data": {
    "product_id": 1001,
    "created_at": "2025-12-04 10:30:00"
  }
}
```

---

### 2.2 获取商品列表

**接口地址**: `/product/list`

**请求方式**: `GET`

**是否需要登录**: 否

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20，最大100 |
| category | string | 否 | 分类筛选 |
| keyword | string | 否 | 关键词搜索（标题/描述） |
| min_price | decimal | 否 | 最低价格 |
| max_price | decimal | 否 | 最高价格 |
| status | int | 否 | 状态筛选：1出售中，2已售出 |
| sort | string | 否 | 排序方式：latest(最新)/price_asc(价格升序)/price_desc(价格降序) |

#### 请求示例

```
GET /product/list?category=书籍教材&keyword=数学&min_price=10&max_price=50&page=1&page_size=20&sort=latest
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 156,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "product_id": 1001,
        "title": "二手高等数学教材",
        "description": "九成新，无笔记",
        "price": 25.50,
        "category": "书籍教材",
        "images": ["/static/uploads/product/img1.jpg"],
        "status": 1,
        "view_count": 120,
        "collect_count": 15,
        "seller": {
          "user_id": 2001,
          "nickname": "张三",
          "avatar": "/static/uploads/avatars/avatar1.jpg",
          "credit_score": 98
        },
        "created_at": "2025-12-04 10:30:00"
      }
    ]
  }
}
```

---

### 2.3 获取商品详情

**接口地址**: `/product/detail`

**请求方式**: `GET`

**是否需要登录**: 否

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |

#### 请求示例

```
GET /product/detail?product_id=1001
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "product_id": 1001,
    "title": "二手高等数学教材",
    "description": "九成新，无笔记，配套习题册齐全。适合大一学生使用。",
    "price": 25.50,
    "category": "书籍教材",
    "images": [
      "/static/uploads/product/img1.jpg",
      "/static/uploads/product/img2.jpg"
    ],
    "status": 1,
    "view_count": 120,
    "collect_count": 15,
    "seller": {
      "user_id": 2001,
      "nickname": "张三",
      "avatar": "/static/uploads/avatars/avatar1.jpg",
      "campus": "南校区",
      "dormitory": "1号楼",
      "credit_score": 98
    },
    "created_at": "2025-12-04 10:30:00",
    "updated_at": "2025-12-04 10:30:00"
  }
}
```

#### 错误响应

```json
{
  "code": 404,
  "message": "商品不存在",
  "data": null
}
```

---

### 2.4 获取我的发布

**接口地址**: `/product/my-list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| status | int | 否 | 状态筛选：1出售中，2已售出，0已下架 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 8,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "product_id": 1001,
        "title": "二手高等数学教材",
        "price": 25.50,
        "category": "书籍教材",
        "images": ["/static/uploads/product/img1.jpg"],
        "status": 1,
        "view_count": 120,
        "collect_count": 15,
        "created_at": "2025-12-04 10:30:00",
        "updated_at": "2025-12-04 10:30:00"
      }
    ]
  }
}
```

---

### 2.5 修改商品信息

**接口地址**: `/product/update`

**请求方式**: `POST`

**是否需要登录**: 是

**权限要求**: 仅商品发布者可修改

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |
| title | string | 否 | 商品标题 |
| description | string | 否 | 商品描述 |
| price | decimal | 否 | 价格 |
| category | string | 否 | 分类 |
| images | array | 否 | 图片URL数组 |

#### 请求示例

```json
{
  "product_id": 1001,
  "title": "二手高等数学教材（第七版）",
  "price": 20.00,
  "description": "九成新，无笔记，配套习题册齐全。价格可小刀。"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "product_id": 1001,
    "updated_at": "2025-12-04 14:30:00"
  }
}
```

#### 错误响应

```json
{
  "code": 403,
  "message": "无权限操作",
  "data": null
}
```

---

### 2.6 修改商品状态

**接口地址**: `/product/update-status`

**请求方式**: `POST`

**是否需要登录**: 是

**权限要求**: 仅商品发布者可修改

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |
| status | int | 是 | 状态：1出售中，2已售出，0已下架 |

#### 请求示例

```json
{
  "product_id": 1001,
  "status": 2
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "状态更新成功",
  "data": {
    "product_id": 1001,
    "status": 2,
    "updated_at": "2025-12-04 14:30:00"
  }
}
```

---

### 2.7 删除商品

**接口地址**: `/product/delete`

**请求方式**: `POST`

**是否需要登录**: 是

**权限要求**: 仅商品发布者可删除

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |

#### 请求示例

```json
{
  "product_id": 1001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "删除成功",
  "data": true
}
```

---

### 2.8 上传商品图片

**接口地址**: `/product/upload-image`

**请求方式**: `POST`

**是否需要登录**: 是

**Content-Type**: `multipart/form-data`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | file | 是 | 图片文件 (jpg, png, jpeg) |

#### 响应示例

```json
{
  "code": 200,
  "message": "上传成功",
  "data": {
    "image_url": "/static/uploads/product/unique_filename.jpg"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "文件格式不支持",
  "data": null
}
```

---

### 2.9 设置商品封面

**接口地址**: `/product/set-cover`

**请求方式**: `POST`

**是否需要登录**: 是

**权限要求**: 仅商品发布者可设置

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |
| image_id | int | 是 | 图片ID |

#### 请求示例

```json
{
  "product_id": 1001,
  "image_id": 5023
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "封面设置成功",
  "data": {
    "image_id": 5023
  }
}
```

#### 错误响应

```json
{
  "code": 403,
  "message": "无权限操作",
  "data": null
}
```

```json
{
  "code": 404,
  "message": "图片不存在",
  "data": null
}
```

---

## 附录

### JWT Token 说明

Token采用JWT格式，包含以下信息：

```json
{
  "user_id": 1001,
  "username": "zhangsan",
  "exp": 1700654400,
  "iat": 1700647200
}
```

### 密码加密

- 使用 werkzeug.security 的 scrypt 算法加密存储
- 密码哈希字段长度：255字符

### Token过期时间

- 访问令牌(access_token)：2小时

### 图片上传限制

- 支持格式：jpg, jpeg, png, gif
- 最大尺寸：2MB
- 头像存储路径：`/static/uploads/avatars/`
- 商品图片存储路径：`/static/uploads/product/`

### 商品状态说明

- `0`: 已下架（用户主动下架或管理员下架）
- `1`: 出售中（正常在售）
- `2`: 已售出（交易完成）

### 商品分类

- 书籍教材
- 电子数码
- 生活用品
- 美妆护肤
- 运动器材
- 其他

## 3. 聊天功能模块

### 3.1 获取会话列表

**接口地址**: `/chat/session-list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "session_id": 1001,
        "buyer_id": 3001,
        "seller_id": 4001,
        "last_message": "你好，请问还在吗？",
        "unread_count": 2,
        "updated_at": "2025-12-09 10:30:00"
      }
      {}
    ]
  }
}
```

---

### 3.2 创建/获取会话

**接口地址**: `/chat/get-or-create-session`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |
| seller_id | int | 是 | 卖家用户ID |

#### 请求示例

```json
{
  "product_id": 2001,
  "seller_id": 4001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "session_id": 1001,
    "product_id": 2001,
    "buyer_id": 3001,
    "seller_id": 4001,
    "created_at": "2025-12-08 09:00:00"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "商品不存在",
  "data": {}
}

```

---

### 3.3 获取会话消息列表

**接口地址**: `/chat/message-list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| session_id | int | 是 | 会话ID |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "message_id": 5001,
        "session_id": 1001,
        "sender_id": 3001,
        "receiver_id": 4001,
        "message_type": 0,
        "content": "你好，请问还在吗？",
        "is_read": 1,
        "created_at": "2025-12-09 10:30:00"
      },
      {
        "message_id": 5002,
        "session_id": 1001,
        "sender_id": 4001,
        "receiver_id": 3001,
        "message_type": 1,
        "content": "/static/uploads/chat/image123.jpg",
        "is_read": 0,
        "created_at": "2025-12-09 10:35:00"
      }
    ]
  }
}
```

#### 错误响应

```json
{
  "code": 403,
  "message": "无权限查看该会话",
  "data": {}
}
```

---

### 3.4 发送消息

**接口地址**: `/chat/send-message`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| session_id | int | 是 | 会话ID |
| receiver_id | int | 是 | 接收者ID |
| message_type | int | 是 | 消息类型：0-文本 1-图片 |
| content | string | 是 | 消息内容（文本或图片URL） |

#### 请求示例

```json
{
  "session_id": 1001,
  "receiver_id": 4001,
  "message_type": 0,
  "content": "你好，请问这个商品还在吗？"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "发送成功",
  "data": {
    "message_id": 5003,
    "session_id": 1001,
    "sender_id": 3001,
    "receiver_id": 4001,
    "message_type": 0,
    "content": "你好，请问这个商品还在吗？",
    "is_read": 0,
    "created_at": "2025-12-09 10:40:00"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "消息内容不能为空",
  "data": {}
}
```

---

### 3.5 标记消息为已读

**接口地址**: `/chat/mark-read`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| session_id | int | 是 | 会话ID |

#### 请求示例

```json
{
  "session_id": 1001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "标记成功",
  "data": true
}
```

---

### 3.6 上传聊天图片

**接口地址**: `/chat/upload-image`

**请求方式**: `POST`

**是否需要登录**: 是

**Content-Type**: `multipart/form-data`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | file | 是 | 图片文件（支持jpg, png, jpeg, gif） |

#### 响应示例

```json
{
  "code": 200,
  "message": "上传成功",
  "data": {
    "image_url": "/static/uploads/chat/20251209_103000_abc123.jpg"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "文件格式不支持，仅支持jpg、png、jpeg、gif",
  "data": false
}
```

---

### 3.7 删除会话

**接口地址**: `/chat/delete-session`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| session_id | int | 是 | 会话ID |

#### 请求示例

```json
{
  "session_id": 1001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "删除成功",
  "data": true
}
```

#### 错误响应

```json
{
  "code": 403,
  "message": "无权限删除该会话",
  "data": false
}
```

---

### 3.8 获取未读消息数

**接口地址**: `/chat/unread-count`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

无

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {  
    "sessions": [
      {
        "session_id": 1001,
        "unread_count": 2
      },
      {
        "session_id": 1002,
        "unread_count": 3
      }
    ]
  }
}
```

---

## 4. 收藏模块

### 4.1 添加收藏

**接口地址**: `/favorite/add`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |

#### 请求示例

```json
{
  "product_id": 1001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "收藏成功",
  "data": {
    "favorite_id": 1,
    "created_at": "2025-12-10 10:30:00"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "已收藏该商品",
  "data": false
}
```

---

### 4.2 取消收藏

**接口地址**: `/favorite/cancel`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |

#### 请求示例

```json
{
  "product_id": 1001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "取消收藏成功",
  "data": true
}
```

---

### 4.3 我的收藏列表

**接口地址**: `/favorite/my-list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "favorite_id": 1,
        "product_id": 1001,
        "title": "99新 iPad Air 5",
        "price": 3500.00,
        "category_id": 2,
        "category": "电子数码",
        "status": 0,
        "images": ["/static/uploads/products/image1.jpg"],
        "seller": {
          "user_id": 2001,
          "nickname": "张三",
          "avatar": "/static/uploads/avatars/avatar1.jpg"
        },
        "created_at": "2025-12-10 10:30:00"
      }
    ]
  }
}
```

---

### 4.4 检查是否收藏

**接口地址**: `/favorite/check`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "is_favorited": true,
    "favorite_id": 1
  }
}
```

---

## 5. 关注模块

### 5.1 关注用户

**接口地址**: `/follow/add`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| followee_id | int | 是 | 被关注者用户ID |

#### 请求示例

```json
{
  "followee_id": 2001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "关注成功",
  "data": {
    "follow_id": 1,
    "created_at": "2025-12-10 10:30:00"
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "不能关注自己",
  "data": false
}
```

```json
{
  "code": 400,
  "message": "已关注该用户",
  "data": false
}
```

---

### 5.2 取消关注

**接口地址**: `/follow/cancel`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| followee_id | int | 是 | 被关注者用户ID |

#### 请求示例

```json
{
  "followee_id": 2001
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "取消关注成功",
  "data": true
}
```

---

### 5.3 我的关注列表

**接口地址**: `/follow/following`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 30,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "follow_id": 1,
        "user_id": 2001,
        "username": "zhangsan",
        "nickname": "张三",
        "avatar": "/static/uploads/avatars/avatar1.jpg",
        "bio": "这是我的个人简介",
        "product_count": 15,
        "created_at": "2025-12-10 10:30:00"
      }
    ]
  }
}
```

---

### 5.4 我的粉丝列表

**接口地址**: `/follow/followers`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "follow_id": 2,
        "user_id": 3001,
        "username": "lisi",
        "nickname": "李四",
        "avatar": "/static/uploads/avatars/avatar2.jpg",
        "bio": "买卖二手物品",
        "product_count": 8,
        "created_at": "2025-12-09 15:20:00"
      }
    ]
  }
}
```

---

### 5.5 检查是否关注

**接口地址**: `/follow/check`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| followee_id | int | 是 | 被关注者用户ID |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "is_following": true,
    "follow_id": 1
  }
}
```

---

### 5.6 获取关注统计

**接口地址**: `/follow/stats`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 否 | 用户ID，不传则查询当前用户 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "following_count": 30,
    "followers_count": 50
  }
}
```

---

## 6. 求购模块

### 6.1 发布求购

**接口地址**: `/wanted/publish`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| title | string | 是 | 求购标题，200字以内 |
| description | string | 是 | 详细描述 |
| category_id | int | 是 | 分类ID |
| target_price | float | 否 | 期望价格 |

#### 请求示例

```json
{
  "title": "求购 iPhone 14 Pro",
  "description": "求购一台成色较新的iPhone 14 Pro，256G或以上，无拆修，价格合理即可",
  "category_id": 2,
  "target_price": 5000.00
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "发布成功",
  "data": {
    "wanted_id": 1,
    "created_at": "2025-12-10 10:30:00"
  }
}
```

---

### 6.2 求购列表

**接口地址**: `/wanted/list`

**请求方式**: `GET`

**是否需要登录**: 否

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| category_id | int | 否 | 分类ID筛选 |
| keyword | string | 否 | 搜索关键词 |
| status | int | 否 | 状态筛选，0-求购中 1-已完成 2-已关闭 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "wanted_id": 1,
        "title": "求购 iPhone 14 Pro",
        "description": "求购一台成色较新的iPhone 14 Pro...",
        "category_id": 2,
        "category": "电子数码",
        "target_price": 5000.00,
        "status": 0,
        "user": {
          "user_id": 1001,
          "nickname": "张三",
          "avatar": "/static/uploads/avatars/avatar1.jpg"
        },
        "created_at": "2025-12-10 10:30:00",
        "updated_at": "2025-12-10 10:30:00"
      }
    ]
  }
}
```

---

### 6.3 求购详情

**接口地址**: `/wanted/detail`

**请求方式**: `GET`

**是否需要登录**: 否

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| wanted_id | int | 是 | 求购ID |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "wanted_id": 1,
    "user_id": 1001,
    "title": "求购 iPhone 14 Pro",
    "description": "求购一台成色较新的iPhone 14 Pro，256G或以上，无拆修，价格合理即可",
    "category_id": 2,
    "category": "电子数码",
    "target_price": 5000.00,
    "status": 0,
    "user": {
      "user_id": 1001,
      "nickname": "张三",
      "avatar": "/static/uploads/avatars/avatar1.jpg",
      "campus": "南校区",
      "dormitory": "1号楼"
    },
    "created_at": "2025-12-10 10:30:00",
    "updated_at": "2025-12-10 10:30:00"
  }
}
```

---

### 6.4 我的求购列表

**接口地址**: `/wanted/my-list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| status | int | 否 | 状态筛选，0-求购中 1-已完成 2-已关闭 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 10,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "wanted_id": 1,
        "title": "求购 iPhone 14 Pro",
        "description": "求购一台成色较新的iPhone 14 Pro...",
        "category_id": 2,
        "category": "电子数码",
        "target_price": 5000.00,
        "status": 0,
        "created_at": "2025-12-10 10:30:00",
        "updated_at": "2025-12-10 10:30:00"
      }
    ]
  }
}
```

---

### 6.5 修改求购状态

**接口地址**: `/wanted/update-status`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| wanted_id | int | 是 | 求购ID |
| status | int | 是 | 状态，0-求购中 1-已完成 2-已关闭 |

#### 请求示例

```json
{
  "wanted_id": 1,
  "status": 1
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "状态更新成功",
  "data": true
}
```

---

### 6.6 删除求购

**接口地址**: `/wanted/delete`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| wanted_id | int | 是 | 求购ID |

#### 请求示例

```json
{
  "wanted_id": 1
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "删除成功",
  "data": true
}
```

#### 错误响应

```json
{
  "code": 403,
  "message": "无权限删除该求购",
  "data": false
}
```

---

### 7.1 获取分类列表

**接口地址**: `/category/list`

**请求方式**: `GET`

**是否需要登录**: 否

#### 请求参数

#### 请求示例

```json
{
  "code": 200,
  "message": "获取分类列表成功",
  "data": [
    {
      "category_id": 1,
      "name": "电子产品",
      "parent_id": null,
      "level": 1,
      "sort_order": 1,
      "status": 1,
      "created_at": "2025-12-10 10:00:00"
    },
    {
      "category_id": 2,
      "name": "手机",
      "parent_id": 1,
      "level": 2,
      "sort_order": 1,
      "status": 1,
      "created_at": "2025-12-10 10:00:00"
    },
    {
      "category_id": 3,
      "name": "数码配件",
      "parent_id": 1,
      "level": 2,
      "sort_order": 2,
      "status": 1,
      "created_at": "2025-12-10 10:00:00"
    }
  ]
}
```

#### 错误响应

```json
{
  "code": 500,
  "message": "服务器错误: 数据库连接失败",
  "data": null
}
```


---

## 8. 评价管理模块

### 8.1 创建评价

**接口地址**: `/review/create`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| reviewee_id | int | 是 | 被评价者用户ID |
| product_id | int | 否 | 关联商品ID |
| rating | int | 是 | 评分，1-5分 |
| content | string | 否 | 评价内容 |

#### 请求示例

```json
{
  "reviewee_id": 2001,
  "product_id": 1001,
  "rating": 5,
  "content": "商品完好，卖家态度好，交易顺利！"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "评价成功",
  "data": {
    "review_id": 3001
  }
}
```

---

### 8.2 获取评价详情

**接口地址**: `/review/detail/<review_id>`

**请求方式**: `GET`

**是否需要登录**: 否

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "review_id": 3001,
    "reviewer_id": 1001,
    "reviewer_nickname": "张三",
    "reviewer_avatar": "/static/avatars/user1.jpg",
    "reviewee_id": 2001,
    "reviewee_nickname": "李四",
    "reviewee_avatar": "/static/avatars/user2.jpg",
    "product_id": 1001,
    "product_title": "二手iPad",
    "rating": 5,
    "content": "商品完好，卖家态度好！",
    "created_at": "2025-12-10 15:30:00"
  }
}
```

---

### 8.3 获取我收到的评价

**接口地址**: `/review/list-received`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 15,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "review_id": 3001,
        "reviewer_id": 1001,
        "reviewer_nickname": "张三",
        "reviewer_avatar": "/static/avatars/user1.jpg",
        "rating": 5,
        "content": "交易顺利",
        "product_title": "二手iPad",
        "created_at": "2025-12-10 15:30:00"
      }
    ]
  }
}
```

---

### 8.4 获取我发出的评价

**接口地址**: `/review/list-sent`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

---

### 8.5 获取用户评分统计

**接口地址**: `/review/user-stats/<user_id>`

**请求方式**: `GET`

**是否需要登录**: 否

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "review_count": 28,
    "avg_rating": 4.8
  }
}
```

---

### 8.6 删除评价

**接口地址**: `/review/delete/<review_id>`

**请求方式**: `DELETE`

**是否需要登录**: 是

#### 响应示例

```json
{
  "code": 200,
  "message": "删除成功",
  "data": true
}
```

---

## 9. 举报管理模块

### 9.1 创建举报

**接口地址**: `/report/create`

**请求方式**: `POST`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| reported_id | int | 否 | 被举报用户ID |
| target_type | int | 是 | 举报对象类型：0-商品 1-用户 |
| target_id | int | 是 | 举报对象ID |
| reason | string | 是 | 举报原因 |
| description | string | 否 | 详细描述 |

#### 请求示例

```json
{
  "reported_id": 2001,
  "target_type": 0,
  "target_id": 1001,
  "reason": "虚假宣传",
  "description": "商品描述与实物不符，涉嫌欺诈"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "举报成功",
  "data": {
    "report_id": 4001
  }
}
```

---

### 9.2 获取举报详情

**接口地址**: `/report/detail/<report_id>`

**请求方式**: `GET`

**是否需要登录**: 是

---

### 9.3 获取我的举报列表

**接口地址**: `/report/my-list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

---

### 9.4 获取举报列表（管理员）

**接口地址**: `/report/list`

**请求方式**: `GET`

**是否需要登录**: 是（需管理员权限）

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| status | int | 否 | 处理状态筛选：0-待处理 1-已处理 2-已驳回 |
| target_type | int | 否 | 对象类型筛选：0-商品 1-用户 |

---

### 9.5 处理举报（管理员）

**接口地址**: `/report/handle/<report_id>`

**请求方式**: `POST`

**是否需要登录**: 是（需管理员权限）

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| status | int | 是 | 处理状态：1-已处理 2-已驳回 |
| handle_result | string | 否 | 处理结果说明 |

#### 请求示例

```json
{
  "status": 1,
  "handle_result": "已核实属实，对违规商品下架，对卖家警告处理"
}
```

---

## 10. 管理员模块

### 10.1 管理员登录

**接口地址**: `/admin/login`

**请求方式**: `POST`

**是否需要登录**: 否

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 管理员用户名 |
| password | string | 是 | 管理员密码 |

#### 请求示例

```json
{
  "username": "admin",
  "password": "admin123"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "admin_info": {
      "admin_id": 1,
      "username": "admin",
      "role": 0,
      "status": 1,
      "last_login_time": "2025-12-10 10:00:00",
      "created_at": "2025-12-01 08:00:00"
    }
  }
}
```

---

### 10.2 封禁用户

**接口地址**: `/admin/ban-user/<user_id>`

**请求方式**: `POST`

**是否需要登录**: 是（需管理员权限）

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| reason | string | 否 | 封禁原因，默认"违反平台规定" |

#### 请求示例

```json
{
  "reason": "发布违规商品，屡次不改"
}
```

#### 响应示例

```json
{
  "code": 200,
  "message": "封禁成功",
  "data": true
}
```

**说明**: 封禁用户后，系统会自动向该用户发送通知。

---

### 10.3 解封用户

**接口地址**: `/admin/unban-user/<user_id>`

**请求方式**: `POST`

**是否需要登录**: 是（需管理员权限）

#### 响应示例

```json
{
  "code": 200,
  "message": "解封成功",
  "data": true
}
```

**说明**: 解封用户后，系统会自动向该用户发送通知。

---

### 10.4 发送通知给用户

**接口地址**: `/admin/send-notification`

**请求方式**: `POST`

**是否需要登录**: 是（需管理员权限）

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 接收用户ID |
| type | int | 否 | 通知类型：0-系统 1-账户操作 2-交易 3-评价，默认0 |
| title | string | 是 | 通知标题 |
| content | string | 是 | 通知内容 |
| related_id | int | 否 | 关联对象ID |

#### 请求示例

```json
{
  "user_id": 1001,
  "type": 0,
  "title": "系统维护通知",
  "content": "平台将于明日凌晨2:00-4:00进行系统维护，期间暂停服务。"
}
```

---

## 11. 通知模块

### 11.1 获取通知列表

**接口地址**: `/notification/list`

**请求方式**: `GET`

**是否需要登录**: 是

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| is_read | int | 否 | 是否已读：0-未读 1-已读 |

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 10,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "notification_id": 5001,
        "user_id": 1001,
        "type": 1,
        "title": "账户已解封",
        "content": "您的账户已解封，可以正常使用。",
        "related_id": 1,
        "is_read": 0,
        "created_at": "2025-12-10 16:00:00"
      },
      {
        "notification_id": 5002,
        "user_id": 1001,
        "type": 0,
        "title": "系统维护通知",
        "content": "平台将于明日凌晨进行维护。",
        "related_id": null,
        "is_read": 1,
        "created_at": "2025-12-09 10:00:00"
      }
    ]
  }
}
```

---

### 11.2 标记通知为已读

**接口地址**: `/notification/mark-read/<notification_id>`

**请求方式**: `POST`

**是否需要登录**: 是

#### 响应示例

```json
{
  "code": 200,
  "message": "标记成功",
  "data": true
}
```

---

### 11.3 标记所有通知为已读

**接口地址**: `/notification/mark-all-read`

**请求方式**: `POST`

**是否需要登录**: 是

#### 响应示例

```json
{
  "code": 200,
  "message": "标记成功",
  "data": true
}
```

---

### 11.4 获取未读通知数量

**接口地址**: `/notification/unread-count`

**请求方式**: `GET`

**是否需要登录**: 是

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "count": 3
  }
}
```

---