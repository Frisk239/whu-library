<template>
  <div class="result-page">
    <div class="result-container">
      <div class="result-header">
        <h1>游戏结算</h1>
      </div>

      <div class="result-content">
        <div class="score-section">
          <div class="score-label">最终学习点</div>
          <div class="score-value">{{ score }}</div>
        </div>

        <div class="rating-section">
          <div class="rating-label">获得评级</div>
          <div class="rating-badge" :class="ratingClass">
            {{ rating }}
          </div>
        </div>

        <div class="character-section">
          <div class="character-display">
            <div class="character-emoji">{{ characterEmoji }}</div>
            <div class="character-name">{{ characterName }}</div>
          </div>
        </div>

        <div class="message-section">
          <div class="message-text">{{ messageText }}</div>
        </div>
      </div>

      <div class="action-section">
        <el-button type="primary" size="large" @click="playAgain" class="action-btn">
          再来一局
        </el-button>
        <el-button size="large" @click="backToMenu" class="action-btn">
          返回菜单
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const score = computed(() => {
  const scoreValue = Number(route.query.score)
  return isNaN(scoreValue) ? 0 : scoreValue
})

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

const characterName = computed(() => {
  const rating = getRating(score.value)
  switch (rating) {
    case '挠痒专业户': return '挠痒大师'
    case '普通学生': return '学习新手'
    case '优秀学生': return '学霸'
    case '学习标兵': return '学神'
    case '学习之神': return '学仙'
    default: return '学习者'
  }
})

const messageText = computed(() => {
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
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.result-container {
  background: white;
  border-radius: 20px;
  padding: 60px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.result-header {
  margin-bottom: 40px;
}

.result-header h1 {
  font-size: 36px;
  color: #303133;
  margin: 0;
}

.result-content {
  margin-bottom: 50px;
}

.score-section {
  margin-bottom: 30px;
}

.score-label {
  font-size: 18px;
  color: #606266;
  margin-bottom: 10px;
}

.score-value {
  font-size: 72px;
  font-weight: bold;
  color: #409EFF;
  line-height: 1;
}

.rating-section {
  margin-bottom: 30px;
}

.rating-label {
  font-size: 18px;
  color: #606266;
  margin-bottom: 15px;
}

.rating-badge {
  display: inline-block;
  padding: 15px 30px;
  border-radius: 50px;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.itch-master {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: #fff;
}

.normal-student {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #333;
}

.excellent-student {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: #333;
}

.study-model {
  background: linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%);
  color: #fff;
}

.study-god {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.character-section {
  margin-bottom: 30px;
}

.character-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.character-emoji {
  font-size: 100px;
  animation: bounce 2s infinite;
}

.character-name {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.message-section {
  margin-bottom: 40px;
}

.message-text {
  font-size: 18px;
  color: #606266;
  line-height: 1.6;
}

.action-section {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.action-btn {
  padding: 15px 40px;
  font-size: 18px;
  border-radius: 25px;
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

@media (max-width: 600px) {
  .result-container {
    padding: 40px 20px;
  }

  .score-value {
    font-size: 60px;
  }

  .rating-badge {
    font-size: 20px;
    padding: 12px 24px;
  }

  .character-emoji {
    font-size: 80px;
  }
}
</style>
