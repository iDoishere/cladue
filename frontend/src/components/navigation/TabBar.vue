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
  transition: all 0.2s;
  min-width: 80px;
}

.tab:hover {
  transform: translateY(-3px);
}

.tab:hover .tab-icon {
  transform: scale(1.1);
}

.tab.active .tab-icon {
  transform: scale(1.05);
}

.tab-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: var(--shadow-sm);
}

.icon {
  font-size: 24px;
}

.tab-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color 0.2s;
}

.tab.active .tab-label {
  color: var(--text-primary);
  font-weight: 600;
}

.tab:hover .tab-label {
  color: var(--text-primary);
}

@media (max-width: 600px) {
  .tab-bar {
    gap: 12px;
  }

  .tab {
    min-width: 70px;
    padding: 10px 12px;
  }

  .tab-icon {
    width: 40px;
    height: 40px;
  }

  .icon {
    font-size: 20px;
  }

  .tab-label {
    font-size: 12px;
  }
}
</style>
