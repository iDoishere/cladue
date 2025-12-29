<script setup lang="ts">
import { ref } from 'vue'
import ChatContainer from './components/chat/ChatContainer.vue'
import TabBar from './components/navigation/TabBar.vue'
import ProfileView from './components/chat/ProfileView.vue'
import ProjectsView from './components/chat/ProjectsView.vue'
import SkillsView from './components/chat/SkillsView.vue'
import ContactView from './components/chat/ContactView.vue'
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
const showProfile = ref(false)
const showProjects = ref(false)
const showSkills = ref(false)
const showContact = ref(false)
const isLoading = ref(false)

async function handleTabClick(tab: string) {
  activeTab.value = tab
  inputText.value = ''

  // Reset all views
  showProfile.value = false
  showProjects.value = false
  showSkills.value = false
  showContact.value = false
  showChat.value = false

  // Show appropriate view based on tab
  if (tab === 'Me') {
    showProfile.value = true
  } else if (tab === 'Projects') {
    showProjects.value = true
  } else if (tab === 'Skills') {
    showSkills.value = true
  } else if (tab === 'Contact') {
    showContact.value = true
  } else {
    // For Fun tab, show chat with AI
    showChat.value = true
    const message = `Tell me about ${tab}`

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
    <div class="main-content">
      <!-- Logo with animation -->
      <div class="logo animate-fade-in" style="animation-delay: 0.1s">IC</div>

      <!-- Title - Hide when any content is visible -->
      <div v-if="!showChat && !showProfile && !showProjects && !showSkills && !showContact" class="title-section animate-fade-in" style="animation-delay: 0.2s">
        <p class="greeting">Hey, I'm Ido 👋</p>
        <h1 class="main-title">AI Portfolio</h1>
      </div>

      <!-- Avatar - Hide when any content is visible -->
      <div v-if="!showChat && !showProfile && !showProjects && !showSkills && !showContact" class="avatar-container animate-scale-in" style="animation-delay: 0.3s">
        <div class="avatar-memoji">
          <div class="avatar-placeholder">🧑‍💻</div>
        </div>
      </div>

      <!-- Profile View - Shows when "Me" tab is clicked -->
      <div v-if="showProfile" class="content-wrapper animate-slide-up">
        <ProfileView />
      </div>

      <!-- Projects View - Shows when "Projects" tab is clicked -->
      <div v-if="showProjects" class="content-wrapper animate-slide-up">
        <ProjectsView />
      </div>

      <!-- Skills View - Shows when "Skills" tab is clicked -->
      <div v-if="showSkills" class="content-wrapper animate-slide-up">
        <SkillsView />
      </div>

      <!-- Contact View - Shows when "Contact" tab is clicked -->
      <div v-if="showContact" class="content-wrapper animate-slide-up">
        <ContactView />
      </div>

      <!-- Chat Container - Shows ABOVE tabs when there are messages -->
      <div v-if="showChat && messages.length > 0" class="content-wrapper animate-slide-up">
        <ChatContainer :messages="messages" />
      </div>

      <!-- Input Field -->
      <div class="input-section animate-fade-in" style="animation-delay: 0.4s">
        <input
          v-model="inputText"
          type="text"
          placeholder="Ask me anything..."
          class="chat-input"
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
  background: #fafafa;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  overflow: hidden;
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
}

.logo {
  width: 40px;
  height: 40px;
  background: #000;
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
}

.title-section {
  text-align: center;
  margin-bottom: -10px;
}

.greeting {
  font-size: 20px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 400;
}

.main-title {
  font-size: 72px;
  font-weight: 900;
  color: #000;
  margin: 0;
  letter-spacing: -0.03em;
  line-height: 1;
}

.avatar-container {
  margin: 10px 0;
}

.avatar-memoji {
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.avatar-placeholder {
  font-size: 140px;
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
  padding: 16px 24px;
  border: 2px solid #e8e8e8;
  border-radius: 50px;
  font-size: 15px;
  outline: none;
  transition: all 0.2s;
  background: white;
}

.chat-input:focus {
  border-color: #4A9EFF;
  box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
}

.send-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #4A9EFF;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.send-button:hover {
  background: #3d8ae5;
  transform: scale(1.05);
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
    font-size: 42px;
  }

  .greeting {
    font-size: 16px;
  }

  .avatar-memoji {
    width: 180px;
    height: 180px;
  }

  .avatar-placeholder {
    font-size: 90px;
  }
}
</style>
