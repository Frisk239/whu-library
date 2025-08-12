<template>
  <div class="game-page">
    <div class="game-header">
      <h2>图书馆挠痒大作战</h2>
      <div class="score-display">
        学习点: <span class="score">{{ score }}</span>
      </div>
    </div>

    <div class="game-area">
      <div class="itch-meter">
        <h3>痒值条</h3>
        <el-progress
          :percentage="itchLevel"
          :color="itchColor"
          :stroke-width="20"
          :format="formatItchText"
        />
      </div>

      <div class="monitor-section">
        <div class="monitor" :class="{ 'watching': monitorWatching }">
          <div class="monitor-face">
            <div class="eyes">
              <div class="eye" :class="{ 'watching-eye': monitorWatching }"></div>
              <div class="eye" :class="{ 'watching-eye': monitorWatching }"></div>
            </div>
            <div class="mouth" :class="{ 'watching-mouth': monitorWatching }"></div>
          </div>
          <div class="monitor-status">
            {{ monitorWatching ? '正在偷拍！' : '假装看书' }}
          </div>
        </div>
        <div v-if="monitorWatching" class="warning">
          <el-alert
            title="警告：管理员正在偷拍！"
            type="warning"
            description="不要挠痒，否则会被抓到！"
            :closable="false"
          />
        </div>
      </div>

      <div class="actions">
        <el-button
          type="primary"
          size="large"
          @click="study"
          :disabled="gameOver"
          class="action-btn"
        >
          学习 (+1分)
        </el-button>

        <el-button
          type="warning"
          size="large"
          @mousedown="startTickling"
          @mouseup="stopTickling"
          @mouseleave="stopTickling"
          :disabled="gameOver || monitorWatching"
          class="action-btn tickle-btn"
        >
          长按挠痒 (-2/秒)
        </el-button>
      </div>

      <div v-if="gameOver" class="game-over">
        <h3>游戏结束！</h3>
        <p>最终得分: {{ score }}</p>
        <el-button type="primary" @click="goToResult">查看结果</el-button>
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

const study = () => {
  if (!gameOver.value) {
    score.value++
  }
}

const startTickling = () => {
  if (monitorWatching.value) {
    ElMessage.error('被管理员发现了！游戏结束！')
    endGame()
    return
  }

  if (!gameOver.value) {
    isTickling.value = true
    tickleInterval = window.setInterval(() => {
      itchLevel.value = Math.max(0, itchLevel.value - 2)
    }, 1000)
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
    }
  }
}

const toggleMonitor = () => {
  if (!gameOver.value) {
    monitorWatching.value = !monitorWatching.value

    // 如果正在偷拍，3秒后切换回看书状态
    if (monitorWatching.value) {
      setTimeout(() => {
        if (!gameOver.value) {
          monitorWatching.value = false
        }
      }, 3000)
    }
  }
}

const endGame = () => {
  gameOver.value = true
  stopTickling()
  cleanup()

  // 保存游戏记录
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
        score: score.value
      })
    })
  }

  // 3秒后自动跳转到结果页
  setTimeout(() => {
    router.push({
      path: '/result',
      query: { score: score.value }
    })
  }, 3000)
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
  // 每0.7秒增加痒值
  itchInterval = window.setInterval(increaseItch, 700)

  // 每3-8秒切换监察者状态
  const scheduleNextToggle = () => {
    const delay = Math.random() * 5000 + 3000 // 3-8秒
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
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.game-header {
  text-align: center;
  margin-bottom: 30px;
}

.score-display {
  font-size: 24px;
  color: #409EFF;
}

.score {
  font-weight: bold;
}

.game-area {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.itch-meter {
  margin-bottom: 30px;
}

.monitor-section {
  margin-bottom: 30px;
  text-align: center;
}

.monitor {
  padding: 20px;
  border-radius: 10px;
  background: #f5f7fa;
  transition: all 0.3s ease;
}

.monitor.watching {
  background: #fef0f0;
  border: 2px solid #f56c6c;
}

.monitor-face {
  width: 100px;
  height: 100px;
  margin: 0 auto 10px;
  position: relative;
}

.eyes {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}

.eye {
  width: 20px;
  height: 20px;
  background: #333;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.watching-eye {
  background: #f56c6c;
  transform: scale(1.2);
}

.mouth {
  width: 40px;
  height: 10px;
  background: #333;
  margin: 20px auto 0;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.watching-mouth {
  background: #f56c6c;
  transform: rotate(90deg);
}

.monitor-status {
  font-size: 18px;
  font-weight: bold;
  color: #606266;
}

.warning {
  margin-top: 15px;
}

.actions {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
}

.action-btn {
  padding: 20px 40px;
  font-size: 18px;
}

.tickle-btn {
  background: #E6A23C;
  border-color: #E6A23C;
}

.tickle-btn:hover {
  background: #cf9236;
  border-color: #cf9236;
}

.game-over {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 10px;
}

.game-over h3 {
  color: #f56c6c;
  margin-bottom: 10px;
}

.game-over p {
  font-size: 20px;
  margin-bottom: 15px;
}
</style>
