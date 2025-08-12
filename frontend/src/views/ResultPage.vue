<template>
  <div class="result-page">
    <div class="result-card">
      <h2>游戏结算</h2>

      <div class="result-content">
        <div class="score-display">
          <h3>最终学习点</h3>
          <div class="score-number">{{ score }}</div>
        </div>

        <div class="rating-section">
          <h3>获得评级</h3>
          <div class="rating-badge" :class="ratingClass">
            {{ rating }}
          </div>
          <p class="rating-description">{{ ratingDescription }}</p>
        </div>

        <div class="character-display">
          <div class="character-icon" :class="characterClass">
            {{ characterEmoji }}
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <el-button type="primary" size="large" @click="playAgain">
          再来一局
        </el-button>
        <el-button size="large" @click="backToMenu">
          返回菜单
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const score = computed(() => Number(route.query.score) || 0)

const getRating = (score: number) => {
  if (score <= 10) return '挠痒专业户'
  if (score <= 30) return '普通学生'
  if (score <= 60) return '优秀学生'
  if (score <= 100) return '学习标兵'
  return '学习之神'
}

const rating = computed(() => getRating(score.value))

const ratingClass = computed(() => {
  const rating = getRating(score.value)
  return {
    'itch-master': rating === '挠痒专业户',
    'normal-student': rating === '普通学生',
    'excellent-student': rating === '优秀学生',
    'study-model': rating === '学习标兵',
    'study-god': rating === '学习之神'
  }
})

const characterEmoji = computed(() => {
  const rating = getRating(score.value)
  switch (rating) {
    case '挠痒专业户': return '😅'
    case '普通学生': return '😊'
    case '优秀学生': return '😄'
    case '学习标兵': return '🤓'
    case '学习之神': return '🧠'
    default: return '😊'
  }
})

const characterClass = computed(() => {
  const rating = getRating(score.value)
  return rating.toLowerCase().replace(/\s+/g, '-')
})

const ratingDescription = computed(() => {
  const rating = getRating(score.value)
  switch (rating) {
    case '挠痒专业户':
      return '看来你更适合挠痒呢！下次多坚持学习吧！'
    case '普通学生':
      return '不错的开始！继续努力，你会变得更优秀！'
    case '优秀学生':
      return '太棒了！你已经掌握了学习的诀窍！'
    case '学习标兵':
      return '你是学习的榜样！继续保持！'
    case '学习之神':
      return '你就是学习界的传奇！无人能敌！'
    default:
      return '感谢参与！'
  }
})

const playAgain = () => {
  router.push('/game')
}

const backToMenu = () => {
  router.push('/')
}
</script>

<style scoped>
.result-page {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.result-card {
  background: white;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.result-card h2 {
  color: #303133;
  margin-bottom: 30px;
}

.result-content {
  margin-bottom: 40px;
}

.score-display {
  margin-bottom: 30px;
}

.score-display h3 {
  color: #606266;
  margin-bottom: 10px;
}

.score-number {
  font-size: 48px;
  font-weight: bold;
  color: #409EFF;
}

.rating-section {
  margin-bottom: 30px;
}

.rating-section h3 {
  color: #606266;
  margin-bottom: 15px;
}

.rating-badge {
  display: inline-block;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.itch-master {
  background: #fef0f0;
  color: #f56c6c;
}

.normal-student {
  background: #f0f9ff;
  color: #409EFF;
}

.excellent-student {
  background: #f6ffed;
  color: #52c41a;
}

.study-model {
  background: #fff7e6;
  color: #fa8c16;
}

.study-god {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.rating-description {
  color: #909399;
  font-size: 16px;
}

.character-display {
  margin: 30px 0;
}

.character-icon {
  font-size: 80px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-buttons .el-button {
  padding: 15px 30px;
  font-size: 16px;
}
</style>
