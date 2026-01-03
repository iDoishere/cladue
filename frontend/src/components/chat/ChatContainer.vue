<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const props = defineProps<{
  messages: Message[]
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-container-wrapper {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  background: var(--card-bg);
  border-radius: 32px;
  box-shadow: var(--shadow-lg), 0 0 0 1px var(--border-color);
  padding: 50px;
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
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
  background: var(--bg-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
  transition: background 0.3s ease;
}

.message-bubble {
  padding: 16px 20px;
  border-radius: 20px;
  line-height: 1.6;
  font-size: 15px;
  box-shadow: var(--shadow-sm);
}

.message.user .message-bubble {
  background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-hover) 100%);
  color: white;
  border-bottom-right-radius: 6px;
}

.message.assistant .message-bubble {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-bottom-left-radius: 6px;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
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

/* Scrollbar styling */
.chat-container::-webkit-scrollbar {
  width: 8px;
}

.chat-container::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: var(--text-tertiary);
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
