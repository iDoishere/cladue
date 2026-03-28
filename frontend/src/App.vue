<script setup lang="ts">
import ChatContainer from './components/chat/ChatContainer.vue'
import HeroSection from './components/hero/HeroSection.vue'
import ChatInput from './components/input/ChatInput.vue'
import AppHeader from './components/layout/AppHeader.vue'
import AuroraBackground from './components/layout/AuroraBackground.vue'
import TabBar from './components/navigation/TabBar.vue'
import OnboardingModal from './components/onboarding/OnboardingModal.vue'
import { useChat } from './composables/useChat'
import { useCursorTrail } from './composables/useCursorTrail'

const { trail, onMouseMove } = useCursorTrail()
const { activeTab, messages, inputText, showChat, isLoading, handleTabClick, handleSendMessage } = useChat()
</script>


<template>
  <div class="app" @mousemove="onMouseMove">
    <AuroraBackground :trail="trail" />
    <OnboardingModal />

    <div class="layout">
      <AppHeader />

      <HeroSection v-if="!showChat" />

      <div v-if="showChat" class="chat-wrap slide-up">
        <ChatContainer :messages="messages" :is-loading="isLoading" />
      </div>

      <ChatInput
        v-model="inputText"
        @send="handleSendMessage"
      />

      <div class="tabs-wrap fade-up" style="--delay: 0.4s">
        <TabBar :active-tab="activeTab" @tab-click="handleTabClick" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: #07090f;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.layout {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 780px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 28px 20px 24px;
  gap: 0;
}

.chat-wrap {
  width: 100%;
  flex: 1;
  min-height: 0;
  margin-bottom: 20px;
  max-height: calc(100vh - 320px);
  overflow-y: auto;
  overflow-x: hidden;
}

.tabs-wrap { width: 100%; }

.fade-up {
  animation: fade-up 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: var(--delay, 0s);
}

.slide-up { animation: fade-up 0.5s cubic-bezier(0.22, 1, 0.36, 1) both; }

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
