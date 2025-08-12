# 图书馆挠痒大作战

一个有趣的前端小游戏，结合了学习、挠痒和躲避监察者的元素。

## 游戏介绍

欢迎来到图书馆！在这里，你需要专心学习，但是身上突然开始痒了起来。你需要在学习和挠痒之间找到平衡，小心图书管理员的监视，被抓到挠痒就糟糕了！

## 技术栈

- **前端**: Vue3 + TypeScript + Element Plus
- **后端**: Python Flask
- **数据库**: SQLite
- **用户系统**: 注册/登录/头像上传

## 游戏规则

- 点击"学习"按钮：+1学习点
- 痒值条：每0.7秒自动增加5点，上限100
- 长按"挠痒"按钮：每秒减少2点痒值
- 监察者：随机切换"假装看书"和"正在偷拍"状态
- 偷拍状态下挠痒会被抓到，游戏结束
- 痒值达到100也会游戏结束

## 评级系统

- 0-10分：挠痒专业户
- 11-30分：普通学生
- 31-60分：优秀学生
- 61-100分：学习标兵
- 101+分：学习之神

## 快速开始

### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动后端服务器

```bash
cd backend
python app.py
```

或者双击 `start.bat`

### 3. 安装前端依赖

```bash
cd frontend
npm install
```

### 4. 启动前端开发服务器

```bash
cd frontend
npm run dev
```

或者双击 `start.bat`

### 5. 访问游戏

打开浏览器访问 `http://localhost:5173`

## 项目结构

```
library-tickle-game/
├── backend/           # Flask后端
│   ├── app.py        # 主应用文件
│   ├── requirements.txt
│   └── start.bat     # Windows启动脚本
├── frontend/         # Vue3前端
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── router/   # 路由配置
│   │   └── main.ts   # 入口文件
│   └── start.bat     # Windows启动脚本
├── database/         # SQLite数据库
├── uploads/          # 用户头像上传目录
└── example/          # 设计参考图片
```

## API接口

- POST `/api/register` - 用户注册
- POST `/api/login` - 用户登录
- POST `/api/upload-avatar` - 上传头像
- POST `/api/game-record` - 保存游戏记录
- GET `/api/leaderboard` - 获取排行榜

## 功能特点

- ✅ 用户注册/登录系统
- ✅ 头像上传功能
- ✅ 实时排行榜
- ✅ 游戏记录保存
- ✅ 响应式设计
- ✅ 动画效果
- ✅ 音效提示

## 开发说明

游戏的核心逻辑在 `GamePage.vue` 中实现，包括：
- 痒值系统（定时器控制）
- 监察者AI（随机状态切换）
- 游戏状态管理
- 结果保存

## 注意事项

1. 确保后端服务器先启动（端口5000）
2. 前端开发服务器默认端口5173
3. 数据库文件会自动创建在 `database/game.db`
4. 头像文件保存在 `uploads/avatars/` 目录

## 许可证

MIT License
