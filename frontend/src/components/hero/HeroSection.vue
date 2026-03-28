<script setup lang="ts">
const nameLetters = 'Ido Cohen'.split('')
</script>

<template>
  <div class="hero">
    <div class="avatar-wrap fade-up" style="--delay: 0.1s">
      <div class="avatar-ring"></div>
      <div class="avatar float">🧑‍💻</div>
    </div>
    <div class="hero-text fade-up" style="--delay: 0.2s">
      <p class="eyebrow">AI Portfolio</p>
      <h1 class="name">
        <span
          v-for="(letter, i) in nameLetters"
          :key="i"
          class="name-letter"
          :style="{ '--i': i }"
        >{{ letter === ' ' ? '\u00A0' : letter }}</span>
      </h1>
      <p class="tagline">Ask me about his projects, skills, or how to hire him</p>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  flex: 1;
  justify-content: center;
  padding: 20px 0 36px;
}

.avatar-wrap {
  position: relative;
  width: 120px; height: 120px;
  display: flex; align-items: center; justify-content: center;
}

.avatar-ring {
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, transparent 40%, rgba(124,58,237,0.5) 60%, rgba(79,70,229,0.4) 75%, transparent 90%);
  animation: spin-ring 8s linear infinite;
}

@keyframes spin-ring {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

.avatar {
  width: 112px; height: 112px;
  border-radius: 50%;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(20px);
  display: flex; align-items: center; justify-content: center;
  font-size: 54px;
  position: relative;
  z-index: 1;
}

.float { animation: float 4s ease-in-out infinite; }

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-10px); }
}

.hero-text { text-align: center; }

.eyebrow {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(167, 139, 250, 0.6);
  margin-bottom: 12px;
  font-family: 'Syne', sans-serif;
}

.name {
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: clamp(48px, 8vw, 72px);
  color: #f8f8ff;
  letter-spacing: -2px;
  line-height: 1;
  margin-bottom: 16px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.name-letter {
  display: inline-block;
  animation: letter-in 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: calc(0.3s + var(--i) * 0.04s);
}

.name-letter:hover {
  color: #a78bfa;
  transform: translateY(-4px);
  transition: color 0.2s, transform 0.2s;
}

@keyframes letter-in {
  from { opacity: 0; transform: translateY(24px) rotateX(40deg); }
  to   { opacity: 1; transform: translateY(0) rotateX(0deg); }
}

.tagline {
  font-size: 15px;
  color: rgba(255,255,255,0.38);
  line-height: 1.6;
  max-width: 340px;
  margin: 0 auto;
}

.fade-up {
  animation: fade-up 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: var(--delay, 0s);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .name { font-size: 42px; }
  .avatar { width: 88px; height: 88px; font-size: 42px; }
  .avatar-wrap { width: 96px; height: 96px; }
}
</style>
