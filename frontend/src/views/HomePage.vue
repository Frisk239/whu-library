<template>
  <div class="home-page">
    <!-- 顶部标题区域 -->
    <div class="header-section">
      <h1 class="main-title">图书馆挠痒大作战</h1>
      <p class="subtitle">学习使人快乐，但是...好痒啊！</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-container">
      <!-- 用户信息区域 -->
      <div class="user-section" v-if="currentUser">
        <div class="user-card">
          <div class="user-avatar">
            <img v-if="currentUser.avatar_url" :src="currentUser.avatar_url" alt="avatar" class="avatar">
            <div v-else class="avatar-placeholder">{{ currentUser.username.charAt(0).toUpperCase() }}</div>
          </div>
          <div class="user-info">
            <h3>欢迎回来，{{ currentUser.username }}！</h3>
            <p>准备好开始新的挑战了吗？</p>
          </div>
        </div>
      </div>

      <!-- 游戏介绍卡片 -->
      <div class="intro-section">
        <div class="intro-card">
          <h2>游戏介绍</h2>
          <div class="intro-content">
            <p>欢迎来到图书馆！在这里，你需要专心学习，但是...</p>
            <p>身上突然开始痒了起来！你需要在学习和挠痒之间找到平衡。</p>
            <p>小心图书管理员的监视，被抓到挠痒就糟糕了！</p>
          </div>
          <div class="stats-box">
            <div class="stat-item">
              <span class="stat-number">{{ playStats.total_plays || 0 }}</span>
              <span class="stat-label">总游玩次数</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮区域 -->
      <div class="action-section">
        <div class="action-buttons">
          <el-button
            type="primary"
            size="large"
            @click="startGame"
            class="action-btn start-btn"
            :disabled="!currentUser"
          >
            <span class="btn-icon">🎮</span>
            <span class="btn-text">开始挑战</span>
          </el-button>

          <el-button
            type="success"
            size="large"
            @click="loadLeaderboard"
            class="action-btn rank-btn"
          >
            <span class="btn-icon">🏆</span>
            <span class="btn-text">刷新排行榜</span>
          </el-button>
        </div>

        <div class="auth-section" v-if="!currentUser">
          <p class="auth-prompt">请先登录或注册账号</p>
          <div class="auth-buttons">
            <el-button @click="goToLogin" class="auth-btn login-btn">
              <span class="btn-icon">🔑</span>
              <span class="btn-text">登录</span>
            </el-button>
            <el-button type="primary" @click="goToRegister" class="auth-btn register-btn">
              <span class="btn-icon">📝</span>
              <span class="btn-text">注册</span>
            </el-button>
          </div>
        </div>

        <div class="logout-section" v-if="currentUser">
          <el-button type="danger" @click="logout" class="logout-btn">
            <span class="btn-icon">🚪</span>
            <span class="btn-text">退出登录</span>
          </el-button>
        </div>
      </div>

      <!-- 排行榜区域 -->
      <div class="leaderboard-section">
        <div class="leaderboard-card">
          <h2>🏆 排行榜</h2>
          <p class="leaderboard-subtitle">前10名学习高手</p>
          <div class="leaderboard-list">
            <div
              v-for="(player, index) in leaderboard"
              :key="index"
              class="leaderboard-item"
              :class="{
                'top-1': index === 0,
                'top-2': index === 1,
                'top-3': index === 2
              }"
            >
              <div class="rank">{{ index + 1 }}</div>
              <div class="player-details">
                <div class="player-name">{{ player.username }}</div>
                <div class="player-rating">{{ player.rating }}</div>
              </div>
              <div class="player-score">{{ player.score }}分</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

interface LeaderboardItem {
  username: string
  score: number
  rating: string
  avatar_url?: string
}

interface User {
  id: number
  username: string
  avatar_url?: string
}

const router = useRouter()
const leaderboard = ref<LeaderboardItem[]>([])
const currentUser = ref<User | null>(null)
const playStats = ref({
  total_plays: 0
})

const startGame = () => {
  if (!currentUser.value) {
    ElMessage.warning('请先登录后再开始游戏')
    router.push('/login')
    return
  }
  router.push('/game')
}

const loadLeaderboard = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/leaderboard')
    leaderboard.value = response.data
  } catch (error) {
    console.error('获取排行榜失败:', error)
    ElMessage.error('获取排行榜失败')
  }
}

const loadPlayStats = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/play-count')
    playStats.value = response.data
  } catch (error) {
    console.error('获取游玩统计失败:', error)
  }
}

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const logout = () => {
  localStorage.removeItem('user')
  currentUser.value = null
  ElMessage.success('已退出登录')
}

onMounted(() => {
  const user = localStorage.getItem('user')
  if (user) {
    currentUser.value = JSON.parse(user)
  }
  loadLeaderboard()
  loadPlayStats()
})

// 当页面重新激活时刷新数据
onActivated(() => {
  loadPlayStats()
  loadLeaderboard()
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.main-title {
  font-size: 42px;
  font-weight: bold;
  color: #2d3436;
  margin: 0 0 10px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 20px;
  color: #636e72;
  margin: 0;
}

.main-container {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 30px;
  align-items: center;
}

.user-section {
  width: 100%;
  max-width: 400px;
}

.user-card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.user-avatar {
  margin-bottom: 15px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  font-weight: bold;
  margin: 0 auto;
}

.user-info h3 {
  font-size: 20px;
  color: #2d3436;
  margin: 0 0 5px 0;
}

.user-info p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.intro-section {
  width: 100%;
  max-width: 600px;
}

.intro-card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.intro-card h2 {
  font-size: 24px;
  color: #2d3436;
  margin: 0 0 20px 0;
  text-align: center;
}

.intro-content p {
  font-size: 16px;
  color: #636e72;
  line-height: 1.6;
  margin: 10px 0;
  text-align: center;
}

.stats-box {
  margin-top: 20px;
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.action-section {
  width: 100%;
  max-width: 400px;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 20px;
}

.action-btn {
  padding: 15px 30px;
  font-size: 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: center;
}

.start-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.start-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.rank-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border: none;
  color: white;
}

.auth-section {
  text-align: center;
}

.auth-prompt {
  font-size: 14px;
  color: #909399;
  margin-bottom: 15px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.auth-btn {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.login-btn {
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
}

.register-btn {
  background: #667eea;
  border: none;
  color: white;
}

.logout-btn {
  width: 100%;
  background: #ff6b6b;
  border: none;
  color: white;
}

.btn-icon {
  font-size: 18px;
}

.btn-text {
  font-weight: 500;
}

.leaderboard-section {
  width: 100%;
  max-width: 600px;
}

.leaderboard-card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.leaderboard-card h2 {
  font-size: 24px;
  color: #2d3436;
  margin: 0 0 5px 0;
  text-align: center;
}

.leaderboard-subtitle {
  font-size: 14px;
  color: #909399;
  text-align: center;
  margin: 0 0 20px 0;
}

.leaderboard-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.leaderboard-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.leaderboard-item.top-1 {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}

.leaderboard-item.top-2 {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
}

.leaderboard-item.top-3 {
  background: linear-gradient(135deg, #cd7f32 0%, #daa520 100%);
}

.rank {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #667eea;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  margin-right: 12px;
}

.player-details {
  flex: 1;
}

.player-name {
  font-size: 14px;
  font-weight: 500;
  color: #2d3436;
}

.player-rating {
  font-size: 12px;
  color: #909399;
}

.player-score {
  font-size: 16px;
  font-weight: bold;
  color: #667eea;
}

@media (max-width: 600px) {
  .home-page {
    padding: 10px;
  }

  .main-title {
    font-size: 32px;
  }

  .subtitle {
    font-size: 16px;
  }

  .main-container {
    padding: 0 10px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .auth-buttons {
    flex-direction: column;
  }
}
</style>
