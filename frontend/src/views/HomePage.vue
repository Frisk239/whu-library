<template>
  <div class="home-page">
    <div class="header">
      <h1 class="main-title">图书馆挠痒大作战</h1>
      <p class="subtitle">学习使人快乐，但是...好痒啊！</p>
    </div>

    <div class="intro-section">
      <div class="intro-card">
        <h3>游戏介绍</h3>
        <p>欢迎来到图书馆！在这里，你需要专心学习，但是...</p>
        <p>身上突然开始痒了起来！你需要在学习和挠痒之间找到平衡。</p>
        <p>小心图书管理员的监视，被抓到挠痒就糟糕了！</p>
      </div>
    </div>

    <div class="user-section" v-if="currentUser">
      <div class="user-info">
        <img v-if="currentUser.avatar_url" :src="currentUser.avatar_url" alt="avatar" class="avatar">
        <div class="user-details">
          <h3>{{ currentUser.username }}</h3>
          <p>欢迎回来！</p>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <el-button type="primary" size="large" @click="startGame" class="start-btn">
        开始挑战
      </el-button>
      <el-button type="success" size="large" @click="toggleLeaderboard" class="rank-btn">
        查看排行榜
      </el-button>
    </div>

    <div class="leaderboard-section" v-if="showLeaderboard">
      <h3>排行榜</h3>
      <div class="leaderboard-list">
        <div
          v-for="(player, index) in leaderboard"
          :key="index"
          class="leaderboard-item"
          :class="{ 'top-player': index < 3 }"
        >
          <span class="rank">{{ index + 1 }}</span>
          <img v-if="player.avatar_url" :src="player.avatar_url" alt="avatar" class="player-avatar">
          <span class="username">{{ player.username }}</span>
          <span class="score">{{ player.score }}分</span>
          <span class="rating">{{ player.rating }}</span>
        </div>
      </div>
    </div>

    <div class="auth-buttons" v-if="!currentUser">
      <el-button @click="goToLogin">登录</el-button>
      <el-button type="primary" @click="goToRegister">注册</el-button>
    </div>

    <div class="logout-section" v-if="currentUser">
      <el-button type="danger" @click="logout">退出登录</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
const showLeaderboard = ref(false)
const leaderboard = ref<LeaderboardItem[]>([])
const currentUser = ref<User | null>(null)

const startGame = () => {
  router.push('/game')
}

const toggleLeaderboard = async () => {
  showLeaderboard.value = !showLeaderboard.value
  if (showLeaderboard.value) {
    await loadLeaderboard()
  }
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
})
</script>

<style scoped>
.home-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.header {
  margin-bottom: 40px;
}

.main-title {
  font-size: 36px;
  color: #409EFF;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #666;
}

.intro-section {
  margin-bottom: 40px;
}

.intro-card {
  background: #f5f7fa;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.intro-card h3 {
  color: #303133;
  margin-bottom: 15px;
}

.intro-card p {
  color: #606266;
  line-height: 1.6;
  margin: 10px 0;
}

.user-section {
  margin-bottom: 30px;
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.action-buttons {
  margin-bottom: 30px;
}

.start-btn, .rank-btn {
  margin: 0 10px;
  padding: 15px 30px;
  font-size: 16px;
}

.leaderboard-section {
  margin-top: 30px;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.leaderboard-list {
  max-height: 400px;
  overflow-y: auto;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  background: #f5f7fa;
  border-radius: 5px;
}

.top-player {
  background: #ecf5ff;
  border-left: 4px solid #409EFF;
}

.rank {
  width: 30px;
  font-weight: bold;
  color: #409EFF;
}

.player-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
}

.username {
  flex: 1;
  text-align: left;
}

.score {
  font-weight: bold;
  color: #67C23A;
  margin: 0 10px;
}

.rating {
  color: #E6A23C;
  font-size: 14px;
}

.auth-buttons, .logout-section {
  margin-top: 20px;
}
</style>
