<script setup lang="ts">
import { ref, onMounted } from 'vue'

const showOnboarding = ref(false)

onMounted(() => {
  if (!localStorage.getItem('ido_onboarded')) {
    setTimeout(() => {
      showOnboarding.value = true
      setTimeout(() => dismiss(), 6000)
    }, 600)
  }
})

function dismiss() {
  showOnboarding.value = false
  localStorage.setItem('ido_onboarded', '1')
}
</script>

<template>
  <Transition name="modal">
    <div v-if="showOnboarding" class="modal-backdrop" @click="dismiss">
      <div class="modal-card" @click.stop>
        <button class="modal-close" @click="dismiss">✕</button>
        <div class="modal-glow"></div>
        <p class="modal-eyebrow">👋 Welcome</p>
        <h2 class="modal-title">Hi, I'm Ido's AI assistant</h2>
        <p class="modal-body">
          Ask me <strong>anything</strong> — his experience, projects, skills, or what he's currently building.
          You can even <strong>send Ido an email</strong> directly through our chat.
        </p>
        <div class="modal-features">
          <div class="modal-feature">
            <span class="modal-feature-icon">💬</span>
            <span>Ask me anything</span>
          </div>
          <div class="modal-feature">
            <span class="modal-feature-icon">📧</span>
            <span>Email Ido directly</span>
          </div>
        </div>
        <button class="modal-cta" @click="dismiss">Let's go →</button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(7, 9, 15, 0.6);
  backdrop-filter: blur(12px);
  padding: 20px;
}

.modal-card {
  position: relative;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(124, 58, 237, 0.25);
  border-radius: 24px;
  padding: 40px 36px 32px;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 0 0 1px rgba(124, 58, 237, 0.1), 0 30px 60px rgba(0, 0, 0, 0.5), 0 0 80px rgba(124, 58, 237, 0.12);
  overflow: hidden;
}

.modal-glow {
  position: absolute;
  top: -80px; left: 50%;
  transform: translateX(-50%);
  width: 300px; height: 200px;
  background: radial-gradient(circle, rgba(124, 58, 237, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.modal-close {
  position: absolute;
  top: 16px; right: 16px;
  background: none; border: none;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px; cursor: pointer;
  padding: 4px 8px; border-radius: 6px;
  transition: color 0.2s, background 0.2s;
}
.modal-close:hover { color: rgba(255, 255, 255, 0.7); background: rgba(255, 255, 255, 0.06); }

.modal-eyebrow {
  font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
  color: rgba(167, 139, 250, 0.7); margin-bottom: 10px;
  font-family: 'Syne', sans-serif;
}

.modal-title {
  font-family: 'Syne', sans-serif; font-weight: 800; font-size: 26px;
  color: #f8f8ff; margin-bottom: 14px; line-height: 1.15;
}

.modal-body {
  font-size: 14px; color: rgba(255, 255, 255, 0.5);
  line-height: 1.7; margin-bottom: 24px;
}
.modal-body strong { color: rgba(167, 139, 250, 0.9); font-weight: 600; }

.modal-features { display: flex; gap: 10px; margin-bottom: 28px; }

.modal-feature {
  flex: 1; display: flex; align-items: center; gap: 8px;
  background: rgba(124, 58, 237, 0.08);
  border: 1px solid rgba(124, 58, 237, 0.18);
  border-radius: 12px; padding: 12px 14px;
  font-size: 13px; color: rgba(255, 255, 255, 0.55);
}

.modal-feature-icon { font-size: 18px; flex-shrink: 0; }

.modal-cta {
  width: 100%; padding: 14px; border-radius: 50px;
  background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
  color: white; font-family: 'Syne', sans-serif;
  font-weight: 700; font-size: 15px; border: none; cursor: pointer;
  transition: transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4); letter-spacing: 0.3px;
}
.modal-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(124, 58, 237, 0.55); }
.modal-cta:active { transform: translateY(0); }

.modal-enter-active { animation: modal-in 0.4s cubic-bezier(0.22, 1, 0.36, 1); }
.modal-leave-active { animation: modal-out 0.25s ease-in forwards; }

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.9) translateY(16px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes modal-out {
  from { opacity: 1; transform: scale(1); }
  to   { opacity: 0; transform: scale(0.95); }
}
</style>
