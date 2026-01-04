<script setup lang="ts">
import { ref } from 'vue'
import ChatContainer from './components/chat/ChatContainer.vue'
import TabBar from './components/navigation/TabBar.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import ParticleBackground from './components/backgrounds/ParticleBackground.vue'
import { chatWithAI } from './services/ai.service'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const activeTab = ref('')
const messages = ref<Message[]>([])
const inputText = ref('')
const showChat = ref(false)
const isLoading = ref(false)

// Map tabs to AI prompts
const tabPrompts: Record<string, string> = {
  'Me': 'Tell me about Ido Cohen - who is he and what does he do?',
  'Projects': 'What projects has Ido worked on? Show me his best work.',
  'Skills': 'What are Ido\'s technical skills and expertise levels?',
  'Fun': 'Tell me something fun or interesting about Ido!',
  'Contact': 'How can I contact Ido? What are his contact details?'
}

async function handleTabClick(tab: string) {
  activeTab.value = tab
  inputText.value = ''
  showChat.value = true

  const message = tabPrompts[tab] || `Tell me about ${tab}`

  // Add user message
  messages.value.push({
    role: 'user' as const,
    content: message,
    timestamp: new Date()
  })

  // Get AI response
  isLoading.value = true
  const aiResponse = await chatWithAI(message)
  isLoading.value = false

  // Add AI response
  messages.value.push({
    role: 'assistant' as const,
    content: aiResponse,
    timestamp: new Date()
  })
}

async function handleSendMessage() {
  if (!inputText.value.trim()) return

  showChat.value = true
  const userMessage = inputText.value
  inputText.value = ''

  // Add user message
  messages.value.push({
    role: 'user' as const,
    content: userMessage,
    timestamp: new Date()
  })

  // Get AI response
  isLoading.value = true
  const aiResponse = await chatWithAI(userMessage)
  isLoading.value = false

  // Add AI response
  messages.value.push({
    role: 'assistant' as const,
    content: aiResponse,
    timestamp: new Date()
  })
}
</script>

<template>
  <div class="app">
    <!-- Particle Background -->
    <ParticleBackground />

    <div class="main-content">
      <!-- Header with Logo and Toggles -->
      <div class="header animate-fade-in" style="animation-delay: 0.1s">
        <div class="logo glass">IC</div>
        <div class="header-controls">
          <ThemeToggle />
        </div>
      </div>

      <!-- Title - Hide when chat is visible -->
      <div v-if="!showChat" class="title-section animate-fade-in" style="animation-delay: 0.2s">
        <p class="greeting">Hey, I'm Ido 👋</p>
        <h1 class="main-title">AI Portfolio</h1>
      </div>

      <!-- Avatar - Hide when chat is visible -->
      <div v-if="!showChat" class="avatar-container animate-scale-in" style="animation-delay: 0.3s">
        <div class="avatar-memoji glass-card">
          <div class="avatar-placeholder">🧑‍💻</div>
        </div>
      </div>

      <!-- Chat Container - Shows when there are messages -->
      <div v-if="showChat && messages.length > 0" class="content-wrapper animate-slide-up">
        <ChatContainer :messages="messages" :is-loading="isLoading" />
      </div>

      <!-- Input Field -->
      <div class="input-section animate-fade-in" style="animation-delay: 0.4s">
        <input
          v-model="inputText"
          type="text"
          placeholder="Ask me anything..."
          class="chat-input glass-input"
          @keyup.enter="handleSendMessage"
        />
        <button class="send-button" @click="handleSendMessage">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
          </svg>
        </button>
      </div>

      <!-- Tabs -->
      <div class="animate-fade-in" style="animation-delay: 0.5s">
        <TabBar :active-tab="activeTab" @tab-click="handleTabClick" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  overflow: hidden;
  position: relative;
}

.main-content {
  width: 100%;
  max-width: 1200px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
}

.header-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.logo {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  color: white;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
  border: 1px solid rgba(0, 255, 255, 0.3);
  box-shadow:
    0 0 20px rgba(0, 255, 255, 0.3),
    0 0 40px rgba(255, 0, 255, 0.2),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
  animation: logoPulse 3s ease-in-out infinite;
}

@keyframes logoPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), 0 0 40px rgba(255, 0, 255, 0.2); }
  50% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.5), 0 0 60px rgba(255, 0, 255, 0.3); }
}

.title-section {
  text-align: center;
  margin-bottom: -10px;
}

.greeting {
  font-size: 22px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 12px;
  font-weight: 400;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.main-title {
  font-size: 80px;
  font-weight: 900;
  margin: 0;
  letter-spacing: -0.03em;
  line-height: 1;
  background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ff88 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease infinite;
  filter: drop-shadow(0 0 30px rgba(0, 255, 255, 0.5)) drop-shadow(0 0 60px rgba(255, 0, 255, 0.3));
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.avatar-container {
  margin: 10px 0;
  position: relative;
}

.avatar-container::before {
  content: '';
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: conic-gradient(from 0deg, #00ffff, #ff00ff, #00ff88, #ffd93d, #00ffff);
  border-radius: 50%;
  animation: rotateGlow 4s linear infinite;
  opacity: 0.6;
  filter: blur(20px);
}

@keyframes rotateGlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.avatar-memoji {
  width: 260px;
  height: 260px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 10, 30, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 1;
  box-shadow:
    0 0 40px rgba(0, 255, 255, 0.3),
    0 0 80px rgba(255, 0, 255, 0.2),
    inset 0 0 40px rgba(255, 255, 255, 0.05);
}

.avatar-placeholder {
  font-size: 130px;
  filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
}

.input-section {
  width: 100%;
  max-width: 550px;
  display: flex;
  gap: 12px;
  align-items: center;
  margin: 10px 0;
}

.chat-input {
  flex: 1;
  padding: 18px 28px;
  border-radius: 50px;
  font-size: 16px;
  outline: none;
  background: rgba(10, 10, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.chat-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.chat-input:focus {
  border-color: rgba(0, 255, 255, 0.5);
  box-shadow:
    0 0 20px rgba(0, 255, 255, 0.3),
    0 0 40px rgba(255, 0, 255, 0.2),
    0 4px 30px rgba(0, 0, 0, 0.3);
}

.send-button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00ffff 0%, #ff00ff 100%);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
  box-shadow:
    0 0 20px rgba(0, 255, 255, 0.4),
    0 0 40px rgba(255, 0, 255, 0.3);
  animation: buttonPulse 2s ease-in-out infinite;
}

@keyframes buttonPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.4), 0 0 40px rgba(255, 0, 255, 0.3); }
  50% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.6), 0 0 60px rgba(255, 0, 255, 0.4); }
}

.send-button:hover {
  transform: scale(1.15);
  box-shadow:
    0 0 30px rgba(0, 255, 255, 0.6),
    0 0 60px rgba(255, 0, 255, 0.5);
}

.send-button:active {
  transform: scale(0.95);
}

.content-wrapper {
  width: 100%;
  max-width: 1100px;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
  opacity: 0;
}

.animate-scale-in {
  animation: scaleIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  opacity: 0;
}

.animate-slide-up {
  animation: slideUp 0.5s ease-out forwards;
}

@media (max-width: 768px) {
  .main-title {
    font-size: 48px;
  }

  .greeting {
    font-size: 18px;
  }

  .avatar-memoji {
    width: 180px;
    height: 180px;
  }

  .avatar-placeholder {
    font-size: 90px;
  }

  .header-controls {
    gap: 8px;
  }

  .logo {
    width: 44px;
    height: 44px;
  }
}
</style>
