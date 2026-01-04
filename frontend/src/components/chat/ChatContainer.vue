<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const props = defineProps<{
  messages: Message[]
  isLoading?: boolean
}>()

const chatContainer = ref<HTMLElement>()

// Auto-scroll to bottom when new messages arrive
watch(() => props.messages.length, async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
})
</script>

<template>
  <div class="chat-container-wrapper">
    <div ref="chatContainer" class="chat-container">
      <div class="messages">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role, 'message-animate']"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant'" class="avatar-small">
              🧑‍💻
            </div>
            <div class="message-bubble">
              {{ message.content }}
            </div>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="isLoading" class="message assistant message-animate">
          <div class="message-content">
            <div class="avatar-small">🧑‍💻</div>
            <div class="message-bubble loading-bubble">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-container-wrapper {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: 32px;
  box-shadow: var(--glass-shadow-lg);
  padding: 40px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.chat-container {
  width: 100%;
  flex: 1;
  overflow-y: auto;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.message {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message-content {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  max-width: 90%;
}

.message.user .message-content {
  flex-direction: row-reverse;
}

.avatar-small {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--glass-bg-strong);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.message-bubble {
  padding: 16px 20px;
  border-radius: 20px;
  line-height: 1.6;
  font-size: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #4A9EFF 0%, #8B5CF6 100%);
  color: white;
  border-bottom-right-radius: 6px;
  box-shadow: 0 4px 20px rgba(74, 158, 255, 0.4);
}

.message.assistant .message-bubble {
  background: var(--glass-bg-light);
  backdrop-filter: blur(10px);
  color: var(--glass-text-primary);
  border: 1px solid var(--glass-border-light);
  border-bottom-left-radius: 6px;
  transition: all 0.3s ease;
}

/* Message animation */
@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(15px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message-animate {
  animation: messageSlideIn 0.4s ease-out forwards;
  opacity: 0;
}

/* Typing indicator */
.loading-bubble {
  padding: 16px 24px !important;
}

.typing-indicator {
  display: flex;
  gap: 6px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4A9EFF 0%, #8B5CF6 100%);
  animation: typingBounce 1.4s ease-in-out infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

/* Scrollbar styling */
.chat-container::-webkit-scrollbar {
  width: 8px;
}

.chat-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  .chat-container-wrapper {
    padding: 20px;
    border-radius: 20px;
  }

  .chat-container {
    max-height: 400px;
  }

  .message-content {
    max-width: 95%;
  }

  .message-bubble {
    font-size: 14px;
    padding: 14px 18px;
  }

  .avatar-small {
    width: 36px;
    height: 36px;
    font-size: 20px;
  }
}
</style>
