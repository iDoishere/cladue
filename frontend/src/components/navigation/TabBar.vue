<script setup lang="ts">
defineProps<{
  activeTab: string
}>()

const emit = defineEmits<{
  tabClick: [tab: string]
}>()

const tabs = [
  { name: 'Me', icon: '👤', color: '#14b8a6' },
  { name: 'Projects', icon: '💼', color: '#22c55e' },
  { name: 'Skills', icon: '📚', color: '#8b5cf6' },
  { name: 'Fun', icon: '🎨', color: '#ec4899' },
  { name: 'Contact', icon: '📞', color: '#f59e0b' }
]
</script>

<template>
  <div class="tab-bar">
    <button
      v-for="tab in tabs"
      :key="tab.name"
      :class="['tab', { active: activeTab === tab.name }]"
      @click="emit('tabClick', tab.name)"
    >
      <div class="tab-icon" :style="{ backgroundColor: activeTab === tab.name ? tab.color : 'var(--tab-bg)' }">
        <span class="icon">{{ tab.icon }}</span>
      </div>
      <span class="tab-label">{{ tab.name }}</span>
    </button>
  </div>
</template>

<style scoped>
.tab-bar {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  padding: 18px 28px;
  background: rgba(10, 10, 30, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  box-shadow:
    0 8px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 255, 0.1),
    inset 0 0 30px rgba(255, 255, 255, 0.02);
}

.tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 80px;
}

.tab:hover {
  transform: translateY(-8px);
}

.tab:hover .tab-icon {
  transform: scale(1.15);
  box-shadow:
    0 0 25px rgba(0, 255, 255, 0.5),
    0 0 50px rgba(255, 0, 255, 0.3),
    0 10px 30px rgba(0, 0, 0, 0.4);
}

.tab.active .tab-icon {
  transform: scale(1.1);
  box-shadow:
    0 0 20px rgba(0, 255, 255, 0.4),
    0 0 40px rgba(255, 0, 255, 0.2),
    0 8px 25px rgba(0, 0, 0, 0.3);
}

.tab-icon {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.icon {
  font-size: 26px;
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
}

.tab-label {
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.tab.active .tab-label {
  color: white;
  font-weight: 600;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

.tab:hover .tab-label {
  color: white;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

@media (max-width: 600px) {
  .tab-bar {
    gap: 10px;
    padding: 14px 18px;
  }

  .tab {
    min-width: 55px;
    padding: 6px;
  }

  .tab-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
  }

  .icon {
    font-size: 22px;
  }

  .tab-label {
    font-size: 11px;
  }
}
</style>
