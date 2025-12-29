# CampusTradingPlatform（校园交易平台）

一个面向校园场景的二手交易平台：支持商品发布/浏览/收藏/聊天、求购发布、用户关注与评价、举报与管理员处理、系统通知等。

## 功能概览（已实现）

- 用户与账号
  - 注册/登录/退出登录
  - 获取/更新个人资料
  - 上传头像
  - 修改密码
- 商品（闲置）
  - 发布商品（支持多图）
  - 商品列表（分页、分类、关键词、价格区间、状态、排序；支持按 `user_id` 查询某用户发布）
  - 商品详情
  - 我的商品列表
  - 修改商品信息/状态
  - 删除商品
  - 上传商品图片、设置封面
- 分类
  - 分类列表
- 收藏
  - 收藏/取消收藏
  - 我的收藏列表
  - 检查是否收藏
- 关注
  - 关注/取消关注
  - 我的关注列表、我的粉丝列表
  - 检查是否关注、关注统计
- 求购
  - 发布求购
  - 求购列表/详情
  - 我的求购列表
  - 更新求购状态、删除求购
- 聊天
  - 会话列表
  - 创建/获取会话（基于商品与买卖双方）
  - 消息列表、发送消息
  - 标记已读、未读数统计
  - 上传聊天图片
  - 删除会话
- 评价
  - 创建评价
  - 评价详情
  - 某用户收到的评价列表（通过 `user_id` 查询）
  - 当前用户发出的评价列表
  - 用户评分统计（平均分、评价数）
  - 删除评价（仅评价者本人）
- 举报
  - 创建举报
  - 举报详情
  - 我的举报列表
  - 举报列表/处理/删除（当前代码为“管理员接口（简化）”，建议接入真实权限控制）
- 管理后台与通知
  - 管理员登录（JWT identity 使用 `admin_<id>` 前缀区分）
  - 封禁/解封用户（封禁会写入通知）
  - 管理员发送通知
  - 用户端通知：列表、标记已读/全部已读、未读数
- 其他
  - 健康检查：`GET /health`

## 技术栈

- 前端：Vue 3、Vue Router、Vuex、Element Plus、Axios（`/api` 代理到后端）
- 后端：Flask、Flask-JWT-Extended、Flask-CORS、PyMySQL（SQL helper 方式）
- 数据库：MySQL 5.7+ / 8.0+

## 快速开始（Windows / PowerShell）

### 1) 初始化数据库

- 创建数据库（示例）：

```sql
CREATE DATABASE campus_trading CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

- 执行建表脚本：`backend/docs/create_table.sql`

> 脚本包含：user、category、product、product_image、favorites、follows、wanted、chat_session、chat_message、reviews、reports、admins、notification。

### 2) 启动后端

```powershell
cd .\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

在 `backend/.env` 配置数据库（示例）：

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=campus_trading
JWT_SECRET_KEY=dev-jwt-secret
SECRET_KEY=dev-secret
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
```

启动：

```powershell
python manage.py
```

后端默认地址：`http://localhost:5000`

### 3) 启动前端

```powershell
cd .\frontend
npm install
npm run serve
```

前端默认地址：`http://localhost:8080`

> 前端开发代理见 `frontend/vue.config.js`：`/api -> http://localhost:5000`（重写去掉 `/api` 前缀）。

## 接口与数据库文档

- 后端 API 文档：`backend/docs/api.md`
- 数据库表设计：`backend/docs/table.md`

## 项目文件结构
```
CampusTradingPlatform/
├─ README.md                                # 项目根说明文档（本文件）
├─ backend/                                  # 后端 Flask API 项目
│  ├─ manage.py                              # 启动/管理脚本（应用入口）
│  ├─ README.md                              # 后端相关说明
│  ├─ requirements.txt                       # Python 依赖列表
│  ├─ app/                                   # Flask 应用包
│  │  ├─ __init__.py                         # 应用工厂与蓝图注册（入口）
│  │  ├─ config.py                           # 配置类（DB、JWT、上传目录等）
│  │  ├─ extensions.py                       # Flask 扩展初始化（JWT、CORS 等）
│  │  ├─ static/                              # 静态文件目录
│  │  │  └─ uploads/  # 上传文件目录（avatars, products, chat）
│  │  ├─ routes/                              # Blueprint 路由实现（按功能分文件）
│  │  │  ├─ admin_route.py                    # 管理员相关 API
│  │  │  ├─ auth_route.py                     # 登录/注册/鉴权 API
│  │  │  ├─ category_route.py                 # 分类相关 API
│  │  │  ├─ chat_route.py                     # 聊天/会话相关 API
│  │  │  ├─ favorite_route.py                 # 收藏相关 API
│  │  │  ├─ follow_route.py                   # 关注相关 API
│  │  │  ├─ product_route.py                  # 商品发布/查询 API
│  │  │  ├─ report_route.py                   # 举报相关 API
│  │  │  ├─ review_route.py                   # 评价相关 API
│  │  │  ├─ wanted_route.py                   # 求购相关 API
│  │  ├─ sqls/                                # SQL 封装与数据访问层（按功能分文件）
│  │  │  ├─ admin_sql.py                      # 管理员相关 SQL
│  │  │  ├─ auth_sql.py                       # 用户鉴权相关 SQL
│  │  │  ├─ category_sql.py                   # 分类相关 SQL
│  │  │  ├─ chat_sql.py                       # 聊天会话/消息相关 SQL
│  │  │  ├─ favorite_sql.py                   # 收藏相关 SQL
│  │  │  ├─ follow_sql.py                     # 关注相关 SQL
│  │  │  ├─ product_sql.py                    # 商品相关 SQL
│  │  │  ├─ report_sql.py                     # 举报相关 SQL
│  │  │  ├─ review_sql.py                     # 评价相关 SQL
│  │  │  ├─ wanted_sql.py                     # 求购相关 SQL
│  │  ├─ utils/                               # 工具与辅助函数
│  │  │  ├─ __init__.py
│  │  │  ├─ db_helper.py                      # DB 连接与游标帮助器
│  │  │  ├─ helpers.py                        # 文件保存、校验等通用函数
│  ├─ docs/                                  # 后端文档（API、建表、表设计等）
│  │  ├─ api.md                               # API 文档
│  │  ├─ create_table.sql                     # 建表脚本（数据库模式）
│  │  ├─ readme.md                            # 后端文档补充
│  │  ├─ table.md                             # 表结构说明
│  ├─ migrations/                             # Alembic 迁移脚本
│  │  ├─ alembic.ini
│  │  ├─ env.py
│  │  ├─ README
│  │  ├─ script.py.mako
│  │  ├─ versions/                            # 迁移历史记录脚本
│  │  │  ├─ 713b908be10d_initial_migration.py
│  │  │  ├─ 810ab493b877_increase_password_hash_length.py
│  ├─ __pycache__/                            # Python 编译缓存（自动生成）
├─ frontend/                                 # 前端 Vue.js 项目
│  ├─ babel.config.js                         # Babel 配置
│  ├─ package.json                            # npm 依赖与脚本
│  ├─ vue.config.js                           # Vue CLI 配置（开发代理等）
│  ├─ public/                                 # 公共静态页面
│  │  └─ index.html                           # 前端入口 HTML
│  ├─ src/                                    # 前端源码
│  │  ├─ App.vue                              # 根组件
│  │  ├─ main.js                              # 前端入口（路由、store 挂载）
│  │  ├─ api/                                 # 封装的后端 API 调用模块
│  │  │  ├─ admin.js                          # 管理员相关 API
│  │  │  ├─ auth.js                           # 登录/注册 API
│  │  │  ├─ category.js                       # 分类 API
│  │  │  ├─ chat.js                           # 聊天 API
│  │  │  ├─ favorite.js                       # 收藏 API
│  │  │  ├─ follow.js                         # 关注 API
│  │  │  ├─ product.js                        # 商品 API
│  │  │  ├─ review.js                         # 评价 API
│  │  │  ├─ wanted.js                         # 求购 API
│  │  ├─ assets/                              # 静态样式/图片等
│  │  │  └─ theme.css                         # 主题样式
│  │  ├─ components/                          # 可复用组件
│  │  │  ├─ NavBar.vue                        # 顶部导航组件
│  │  │  ├─ ReviewModal.vue                   # 评价弹窗组件
│  │  ├─ router/                              # 前端路由配置
│  │  │  └─ index.js
│  │  ├─ store/                               # Vuex 状态管理
│  │  │  └─ index.js
│  │  ├─ utils/                               # 前端工具（请求封装等）
│  │  │  └─ request.js                        # Axios 封装
│  │  ├─ views/                               # 页面级视图组件
│  │  │  ├─ AdminLogin.vue                    # 管理员登录页
│  │  │  ├─ AdminPanel.vue                    # 管理后台页
│  │  │  ├─ Chat.vue                          # 聊天页
│  │  │  ├─ Favorites.vue                     # 收藏页
│  │  │  ├─ Follows.vue                       # 关注/粉丝页
│  │  │  ├─ Home.vue                          # 首页/商品列表
│  │  │  ├─ Login.vue                         # 用户登录页
│  │  │  ├─ MyItems.vue                       # 我的商品页
│  │  │  ├─ MyWanted.vue                      # 我的求购页
│  │  │  ├─ ProductDetail.vue                 # 商品详情页
│  │  │  ├─ Profile.vue                       # 个人资料页
│  │  │  ├─ Publish.vue                       # 发布商品页
│  │  │  ├─ Register.vue                      # 注册页
│  │  │  ├─ UserProfile.vue                   # 他人个人页
│  │  │  ├─ WantedDetail.vue                  # 求购详情
│  │  │  ├─ WantedList.vue                    # 求购列表
│  │  │  ├─ WantedPublish.vue                 # 发布求购页
│  │  │  └─ components/                        # 页面内子组件
│  │  │     └─ UserList.vue                    # 用户列表组件
├─ pics/                                     # 项目图片/示例资源目录
```

 

## 备注与约束

- `report` 的“管理员接口”目前仅用 `@jwt_required()` 简化鉴权（未做真实管理员权限校验）；`admin` 相关接口通过 JWT identity 前缀 `admin_` 做区分。
- 文件上传：后端会将上传文件保存到 `backend/app/static/uploads/...`（头像/商品图/聊天图）。
