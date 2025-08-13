<template>
  <div class="game-page">
    <div class="game-container">
      <div class="game-header">
        <h1 class="game-title">图书馆挠痒大作战</h1>
        <div class="score-display">
          <span class="score-label">学习点</span>
          <span class="score-value">{{ score }}</span>
        </div>
      </div>

      <div class="game-content">
        <div class="itch-section">
          <h3 class="section-title">痒值条</h3>
          <div class="progress-container">
            <el-progress
              :percentage="itchLevel"
              :color="itchColor"
              :stroke-width="25"
              :format="formatItchText"
              class="itch-progress"
            />
            <div class="progress-labels">
              <span>0</span>
              <span>50</span>
              <span>100</span>
            </div>
          </div>
        </div>

        <div class="monitor-section" :class="{ 'warning-mode': monitorWatching }">
          <div class="monitor-card">
            <div class="monitor-avatar" :class="{ 'watching': monitorWatching }">
              <div class="eyes">
                <div class="eye" :class="{ 'watching-eye': monitorWatching }"></div>
                <div class="eye" :class="{ 'watching-eye': monitorWatching }"></div>
              </div>
              <div class="mouth" :class="{ 'watching-mouth': monitorWatching }"></div>
            </div>
            <div class="monitor-status">
              <span class="status-text">{{ monitorWatching ? '⚠️ 正在偷拍！' : '📚 假装看书' }}</span>
            </div>
          </div>
        </div>

        <div class="actions-section">
          <div class="action-card">
            <el-button
              type="primary"
              size="large"
              @click="study"
              :disabled="gameOver"
              class="action-btn study-btn"
            >
              <span class="btn-icon">📖</span>
              <span class="btn-text">学习</span>
              <span class="btn-subtext">+1分</span>
            </el-button>
          </div>

          <div class="action-card">
            <el-button
              type="warning"
              size="large"
              @mousedown="startTickling"
              @mouseup="stopTickling"
              @mouseleave="stopTickling"
              @touchstart.prevent="startTickling"
              @touchend.prevent="stopTickling"
              :disabled="gameOver"
              class="action-btn tickle-btn"
            >
              <span class="btn-icon">🤏</span>
              <span class="btn-text">挠痒</span>
              <span class="btn-subtext">-6/0.6秒</span>
            </el-button>
          </div>
        </div>

        <div v-if="gameOver" class="game-over-modal">
          <div class="modal-content">
            <h2>游戏结束！</h2>
            <p class="final-score">最终得分: {{ score }}</p>
            <el-button type="primary" @click="goToResult" class="result-btn">
              查看结果
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const score = ref(0)
const itchLevel = ref(0)
const monitorWatching = ref(false)
const gameOver = ref(false)
const isTickling = ref(false)

let itchInterval: number | null = null
let monitorInterval: number | null = null
let tickleInterval: number | null = null

const itchColor = (percentage: number) => {
  if (percentage < 30) return '#67C23A'
  if (percentage < 70) return '#E6A23C'
  return '#F56C6C'
}

const formatItchText = (percentage: number) => {
  return `${percentage}/100`
}

const study = (event: MouseEvent) => {
  if (!gameOver.value) {
    score.value++
    // 创建自定义消息，从按钮位置弹出
    const message = document.createElement('div')
    message.className = 'floating-message'
    message.textContent = '+1 学习点！'
    message.style.cssText = `
      position: fixed;
      top: ${event.clientY - 50}px;
      left: ${event.clientX - 30}px;
      background: #67C23A;
      color: white;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: bold;
      z-index: 9999;
      animation: floatUp 1s ease-out forwards;
      pointer-events: none;
    `

    const style = document.createElement('style')
    style.textContent = `
      @keyframes floatUp {
        0% {
          opacity: 1;
          transform: translateY(0);
        }
        100% {
          opacity: 0;
          transform: translateY(-30px);
        }
      }
    `
    document.head.appendChild(style)
    document.body.appendChild(message)

    setTimeout(() => {
      message.remove()
      style.remove()
    }, 1000)
  }
}

const startTickling = () => {
  if (!gameOver.value) {
    isTickling.value = true

    tickleInterval = window.setInterval(() => {
      if (monitorWatching.value && isTickling.value) {
        ElMessage.error('被杨xx偷拍到了！游戏结束！')
        endGame()
        return
      }

      itchLevel.value = Math.max(0, itchLevel.value - 6)

      if (itchLevel.value === 0) {
        ElMessage.success('不痒了！')
      }
    }, 600)
  }
}

const stopTickling = () => {
  isTickling.value = false
  if (tickleInterval) {
    clearInterval(tickleInterval)
    tickleInterval = null
  }
}

const increaseItch = () => {
  if (!gameOver.value) {
    itchLevel.value = Math.min(100, itchLevel.value + 5)

    if (itchLevel.value >= 100) {
      ElMessage.error('太痒了！无法继续学习！')
      endGame()
    } else if (itchLevel.value >= 80) {
      ElMessage.warning('好痒啊！')
    }
  }
}

const toggleMonitor = () => {
  if (!gameOver.value) {
    monitorWatching.value = !monitorWatching.value

    if (monitorWatching.value) {
      ElMessage.warning('杨xx开始偷拍了！小心被诬告！')

      setTimeout(() => {
        if (!gameOver.value) {
          monitorWatching.value = false
          ElMessage.success('杨xx假装继续看书了')
        }
      }, 3000)
    }
  }
}

const endGame = () => {
  gameOver.value = true
  stopTickling()
  cleanup()

  const user = localStorage.getItem('user')
  if (user) {
    const userData = JSON.parse(user)
    fetch('http://localhost:5000/api/game-record', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userData.id,
        score: score.value,
      })
    })
  }
}

const goToResult = () => {
  router.push({
    path: '/result',
    query: { score: score.value }
  })
}

const cleanup = () => {
  if (itchInterval) clearInterval(itchInterval)
  if (monitorInterval) clearInterval(monitorInterval)
  if (tickleInterval) clearInterval(tickleInterval)
}

onMounted(() => {
  itchInterval = window.setInterval(increaseItch, 700)

  const scheduleNextToggle = () => {
    const delay = Math.random() * 5000 + 3000
    monitorInterval = window.setTimeout(() => {
      if (!gameOver.value) {
        toggleMonitor()
        scheduleNextToggle()
      }
    }, delay)
  }
  scheduleNextToggle()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
.game-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.game-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.game-header {
  text-align: center;
  margin-bottom: 40px;
}

.game-title {
  font-size: 32px;
  color: #2d3436;
  margin: 0 0 20px 0;
}

.score-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.score-label {
  font-size: 18px;
  color: #636e72;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  color: #0984e3;
}

.game-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.section-title {
  font-size: 20px;
  color: #2d3436;
  margin: 0 0 15px 0;
  text-align: center;
}

.progress-container {
  position: relative;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 12px;
  color: #636e72;
}

.itch-progress {
  margin-bottom: 10px;
}

.monitor-section {
  transition: all 0.3s ease;
}

.monitor-section.warning-mode {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.monitor-card {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  transition: all 0.3s ease;
}

.monitor-section.warning-mode .monitor-card {
  background: #fff5f5;
  border: 2px solid #f56565;
}

.monitor-avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 15px;
  position: relative;
}

.eyes {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.eye {
  width: 16px;
  height: 16px;
  background: #333;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.watching-eye {
  background: #f56565;
  transform: scale(1.3);
}

.mouth {
  width: 30px;
  height: 8px;
  background: #333;
  margin: 15px auto 0;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.watching-mouth {
  background: #f56565;
  transform: rotate(90deg);
}

.monitor-status {
  margin-top: 15px;
}

.status-text {
  font-size: 18px;
  font-weight: bold;
  color: #2d3436;
}

.actions-section {
  display: flex;
  justify-content: space-around;
  gap: 20px;
  margin-top: 40px;
}

.action-card {
  flex: 1;
}

.action-btn {
  width: 100%;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 15px;
  font-size: 16px;
}

.btn-icon {
  font-size: 24px;
}

.btn-text {
  font-size: 18px;
  font-weight: bold;
}

.btn-subtext {
  font-size: 12px;
  opacity: 0.8;
}

.study-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.tickle-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border: none;
  color: white;
}

.game-over-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  color: #2d3436;
  margin-bottom: 20px;
}

.final-score {
  font-size: 24px;
  color: #0984e3;
  margin-bottom: 20px;
}

.result-btn {
  padding: 15px 30px;
  font-size: 18px;
}

@media (max-width: 600px) {
  .game-container {
    padding: 20px;
    margin: 10px;
  }

  .game-title {
    font-size: 28px;
  }

  .actions-section {
    flex-direction: column;
  }

  .action-btn {
    height: 100px;
  }
}
</style>
