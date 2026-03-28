<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import VueMarkdownIt from 'vue3-markdown-it'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const props = defineProps<{
  messages: Message[]
  isLoading?: boolean
}>()

const messagesEnd = ref<HTMLElement>()

function scrollToBottom() {
  nextTick(() => {
    messagesEnd.value?.scrollIntoView({ behavior: 'smooth' })
  })
}

watch(() => props.messages.length, scrollToBottom)
watch(() => props.isLoading, scrollToBottom)
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
              <VueMarkdownIt v-if="message.role === 'assistant'" :source="message.content" />
              <span v-else>{{ message.content }}</span>
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

        <div ref="messagesEnd"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-container-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-container {
  width: 100%;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 16px;
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

@keyframes msg-from-right {
  from { opacity: 0; transform: translateX(20px) translateY(6px); }
  to   { opacity: 1; transform: translateX(0) translateY(0); }
}
@keyframes msg-from-left {
  from { opacity: 0; transform: translateX(-20px) translateY(6px); }
  to   { opacity: 1; transform: translateX(0) translateY(0); }
}

.message.user.message-animate {
  animation: msg-from-right 0.35s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  opacity: 0;
}
.message.assistant.message-animate {
  animation: msg-from-left 0.35s cubic-bezier(0.22, 1, 0.36, 1) forwards;
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

/* Markdown rendering inside assistant bubbles */
.message.assistant .message-bubble h1,
.message.assistant .message-bubble h2,
.message.assistant .message-bubble h3 {
  font-weight: 700;
  margin: 10px 0 4px;
  color: var(--glass-text-primary);
}
.message.assistant .message-bubble h2 { font-size: 15px; }
.message.assistant .message-bubble h3 { font-size: 14px; }

.message.assistant .message-bubble ul,
.message.assistant .message-bubble ol {
  padding-left: 18px;
  margin: 6px 0;
}
.message.assistant .message-bubble li {
  margin: 3px 0;
}
.message.assistant .message-bubble strong {
  font-weight: 700;
  color: #4A9EFF;
}
.message.assistant .message-bubble code {
  background: rgba(255,255,255,0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: monospace;
}
.message.assistant .message-bubble p {
  margin: 4px 0;
}
.message.assistant .message-bubble p:first-child { margin-top: 0; }
.message.assistant .message-bubble p:last-child { margin-bottom: 0; }

/* Scrollbar styling */
.chat-container::-webkit-scrollbar {
  width: 3px;
}

.chat-container::-webkit-scrollbar-track {
  background: linear-gradient(180deg,
    transparent 0%,
    rgba(124, 58, 237, 0.04) 30%,
    rgba(124, 58, 237, 0.04) 70%,
    transparent 100%
  );
  border-radius: 100px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg,
    rgba(167, 139, 250, 0.9) 0%,
    rgba(124, 58, 237, 0.8) 40%,
    rgba(79, 70, 229, 0.7) 100%
  );
  border-radius: 100px;
  box-shadow:
    0 0 6px rgba(124, 58, 237, 0.8),
    0 0 12px rgba(124, 58, 237, 0.4),
    0 0 20px rgba(124, 58, 237, 0.2);
  transition: box-shadow 0.3s ease, background 0.3s ease;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg,
    #c4b5fd 0%,
    #a78bfa 40%,
    #7c3aed 100%
  );
  box-shadow:
    0 0 8px rgba(167, 139, 250, 1),
    0 0 18px rgba(124, 58, 237, 0.7),
    0 0 30px rgba(124, 58, 237, 0.4);
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
