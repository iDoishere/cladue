<script setup lang="ts">
</script>

<template>
  <header class="header fade-up" style="--delay: 0s">
    <div class="logo">IC</div>
    <div class="header-right">
      <span class="status-dot"></span>
      <span class="status-text">Available for work</span>
    </div>
  </header>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.logo {
  width: 42px; height: 42px;
  border-radius: 12px;
  background: rgba(124, 58, 237, 0.12);
  border: 1px solid rgba(124, 58, 237, 0.25);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: 15px;
  color: rgba(167, 139, 250, 0.9);
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 8px rgba(52, 211, 153, 0.6);
  animation: pulse-dot 2.5s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(52,211,153,0.6); }
  50%       { opacity: 0.6; box-shadow: 0 0 3px rgba(52,211,153,0.3); }
}

.status-text {
  font-size: 12px;
  color: rgba(255,255,255,0.35);
  letter-spacing: 0.3px;
}

.fade-up {
  animation: fade-up 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: var(--delay, 0s);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
