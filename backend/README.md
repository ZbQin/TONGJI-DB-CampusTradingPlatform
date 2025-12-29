# 校园交易平台 - 后端（Flask）

本目录为校园交易平台后端 API 服务，基于 Flask + JWT + PyMySQL（SQL helper 方式）。

> 项目整体说明与完整功能清单请看仓库根目录：`README.md`。

## 环境要求

- Python 3.9 / 3.10 / 3.11
- MySQL 5.7+ 或 8.0+

## 安装与运行（Windows / PowerShell）

```powershell
cd .\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

在 `backend/.env` 配置数据库连接（后端会自动读取）：

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

初始化数据库：执行 `docs/create_table.sql`（包含所有表）。

启动：

```powershell
python manage.py
```

健康检查：`GET http://localhost:5000/health`

## 文档

- API 文档：`docs/api.md`
- 数据库表：`docs/table.md`

## 目录说明（当前结构）

- `manage.py`：启动入口
- `app/`：应用工厂、配置、路由、SQL、工具
- `app/routes/`：接口路由（auth/product/category/wanted/favorite/follow/chat/review/report/admin/notification）
- `app/sqls/`：SQL 层封装
- `docs/`：文档与建表脚本
