# 图书馆挠痒大作战

一个前端小游戏，灵感来自b站up主小毛毛熊，以及武大图书馆诬告事件。

## 技术栈

- **前端**: Vue3 + TypeScript + Element Plus
- **后端**: Python Flask
- **数据库**: SQLite
- **部署**: Nginx + Sakura Frp
- **用户系统**: 注册/登录

## 快速开始

### 1. 本地开发运行

```bash
# 克隆项目
git clone https://github.com/Frisk239/whu-library.git
cd whu-library

# 启动后端
cd backend
pip install -r requirements.txt
python app.py || start.bat


# 启动前端
cd ../frontend
npm install
npm run dev || start.bat


# 访问游戏
http://localhost:3000
```

### 2. 生产环境部署

#### 2.1 安装依赖

```bash
# 前端构建
cd frontend
npm install
npm run build

# 后端依赖
cd ../backend
pip install -r requirements.txt
```

#### 2.2 配置Nginx

1. 安装Nginx
2. 将项目中的`nginx-whu-library.conf`复制到Nginx的`conf.d`目录
3. 修改配置中的路径为实际项目路径
4. 重启Nginx

示例Nginx配置：
```nginx
server {
    listen 80;
    server_name _;
    
    # CORS配置
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
    add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept";
    
    # 前端静态文件
    location / {
        root /path/to/whu-library/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 2.3 启动服务

```bash
# 启动后端
cd backend
python app.py --host=0.0.0.0 --port=5000

# 访问游戏
http://your-server-ip
```

### 3. 使用Sakura Frp实现公网访问

1. 注册并登录Sakura Frp (https://www.natfrp.com/)
2. 下载对应系统的客户端
3. 创建隧道配置：
   - 本地IP: 127.0.0.1
   - 本地端口: 80 (Nginx端口)
   - 选择服务器节点
4. 启动Frp客户端
5. 启动Nginx
6. 访问Frp提供的公网地址(如https://frp-rug.com:16780)

## 项目结构

```
whu-library/
├── backend/           # Flask后端
│   ├── app.py        # 主应用文件
│   ├── requirements.txt
│   └── start.bat     # Windows启动脚本
├── frontend/         # Vue3前端
│   ├── dist/         # 生产构建输出
│   ├── src/          # 源代码
│   └── vite.config.ts # 构建配置
├── nginx-whu-library.conf # Nginx配置
└── README.md         # 项目文档
```

## API接口

- POST `/api/register` - 用户注册
- POST `/api/login` - 用户登录
- POST `/api/game-record` - 保存游戏记录
- GET `/api/leaderboard` - 获取排行榜

## 注意事项

1. 生产环境建议使用Gunicorn运行Flask应用：
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. 如需HTTPS支持，可申请SSL证书并配置Nginx

3. 文件上传目录需要写权限：
   ```bash
   chmod -R 777 backend/uploads
   ```

## 许可证

MIT License
