<script setup lang="ts">
const props = defineProps<{
  modelValue: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'send': []
}>()

function onInput(e: Event) {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}
</script>

<template>
  <div class="input-wrap fade-up" style="--delay: 0.3s">
    <div class="input-row">
      <input
        :value="props.modelValue"
        type="text"
        placeholder="Ask me anything about Ido..."
        class="input"
        @input="onInput"
        @keyup.enter="emit('send')"
      />
      <button
        class="send-btn"
        @click="emit('send')"
        :disabled="!props.modelValue.trim()"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.input-wrap {
  width: 100%;
  margin-bottom: 16px;
}

.input-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.input {
  flex: 1;
  padding: 16px 22px;
  border-radius: 50px;
  font-size: 15px;
  outline: none;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.9);
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.input::placeholder { color: rgba(255,255,255,0.22); }

.input:focus {
  border-color: rgba(124,58,237,0.5);
  box-shadow: 0 0 0 3px rgba(124,58,237,0.1);
}

.send-btn {
  width: 50px; height: 50px;
  border-radius: 50%;
  background: #7c3aed;
  color: white;
  border: none;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: transform 0.15s, background 0.15s, opacity 0.15s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) { background: #6d28d9; transform: scale(1.06); }
.send-btn:active:not(:disabled) { transform: scale(0.96); }
.send-btn:disabled { opacity: 0.35; cursor: not-allowed; }

.fade-up {
  animation: fade-up 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: var(--delay, 0s);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
