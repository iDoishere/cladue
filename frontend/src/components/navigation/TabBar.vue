<script setup lang="ts">
defineProps<{ activeTab: string }>()

const emit = defineEmits<{ tabClick: [tab: string] }>()

const tabs = [
  { name: 'Me',       icon: '👤' },
  { name: 'Projects', icon: '💼' },
  { name: 'Skills',   icon: '⚡' },
  { name: 'Fun',      icon: '✦'  },
  { name: 'Contact',  icon: '→'  },
]
</script>

<template>
  <div class="tab-bar">
    <button
      v-for="(tab, i) in tabs"
      :key="tab.name"
      :class="['tab', { active: activeTab === tab.name }]"
      :style="{ '--i': i }"
      @click="emit('tabClick', tab.name)"
    >
      <span class="tab-icon">{{ tab.icon }}</span>
      <span class="tab-label">{{ tab.name }}</span>
    </button>
  </div>
</template>

<style scoped>
.tab-bar {
  display: flex;
  gap: 6px;
  justify-content: center;
  padding: 6px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px;
  backdrop-filter: blur(16px);
}

.tab {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 16px;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: background 0.18s, transform 0.15s, color 0.18s;
  color: rgba(255,255,255,0.45);
  animation: tab-in 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: calc(0.5s + var(--i) * 0.07s);
}

@keyframes tab-in {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.tab:hover {
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.75);
  transform: translateY(-1px);
}

.tab.active {
  background: rgba(124,58,237,0.18);
  border: 1px solid rgba(124,58,237,0.25);
  color: #c4b5fd;
}

.tab-icon {
  font-size: 15px;
  line-height: 1;
}

.tab-label {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.2px;
}

@media (max-width: 520px) {
  .tab-label { display: none; }
  .tab { padding: 10px 14px; }
  .tab-icon { font-size: 18px; }
}
</style>
