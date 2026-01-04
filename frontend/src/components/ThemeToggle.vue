<script setup lang="ts">
import { computed } from 'vue'
import { useTheme } from '../composables/useTheme'

const { isDark, toggle } = useTheme()

const ariaLabel = computed(() =>
  isDark.value ? 'Switch to light mode' : 'Switch to dark mode'
)
</script>

<template>
  <button
    class="theme-toggle"
    :class="{ 'theme-toggle--dark': isDark }"
    :aria-label="ariaLabel"
    title="Toggle theme"
    @click="toggle"
  >
    <svg
      class="theme-toggle__svg"
      aria-hidden="true"
      width="24"
      height="24"
      viewBox="0 0 24 24"
    >
      <!-- Sun core -->
      <circle
        class="theme-toggle__sun"
        cx="12"
        cy="12"
        r="5"
        fill="currentColor"
      />

      <!-- Sun rays -->
      <g class="theme-toggle__rays" fill="currentColor">
        <circle cx="12" cy="2" r="1.5" />
        <circle cx="12" cy="22" r="1.5" />
        <circle cx="2" cy="12" r="1.5" />
        <circle cx="22" cy="12" r="1.5" />
        <circle cx="4.93" cy="4.93" r="1.5" />
        <circle cx="19.07" cy="4.93" r="1.5" />
        <circle cx="4.93" cy="19.07" r="1.5" />
        <circle cx="19.07" cy="19.07" r="1.5" />
      </g>

      <!-- Moon mask (eclipse effect) -->
      <circle
        class="theme-toggle__moon"
        cx="18"
        cy="6"
        r="8"
        fill="var(--bg-primary)"
      />
    </svg>
  </button>
</template>

<style scoped>
.theme-toggle {
  --toggle-size: 50px;

  position: relative;
  width: var(--toggle-size);
  height: var(--toggle-size);
  padding: 0;
  background: linear-gradient(135deg, rgba(255, 200, 50, 0.15) 0%, rgba(255, 150, 0, 0.15) 100%);
  border: 1px solid rgba(255, 200, 50, 0.3);
  border-radius: 50%;
  cursor: pointer;
  color: #ffd93d;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 0 15px rgba(255, 200, 50, 0.3),
    0 0 30px rgba(255, 150, 0, 0.15);
}

.theme-toggle--dark {
  background: linear-gradient(135deg, rgba(100, 150, 255, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
  border-color: rgba(139, 92, 246, 0.3);
  color: #a29bfe;
  box-shadow:
    0 0 15px rgba(139, 92, 246, 0.3),
    0 0 30px rgba(100, 150, 255, 0.15);
}

.theme-toggle:hover {
  transform: scale(1.1);
  box-shadow:
    0 0 25px rgba(255, 200, 50, 0.5),
    0 0 50px rgba(255, 150, 0, 0.25);
}

.theme-toggle--dark:hover {
  box-shadow:
    0 0 25px rgba(139, 92, 246, 0.5),
    0 0 50px rgba(100, 150, 255, 0.25);
}

.theme-toggle:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}

.theme-toggle__svg {
  width: 26px;
  height: 26px;
  overflow: visible;
  filter: drop-shadow(0 0 5px currentColor);
}

/* Sun core */
.theme-toggle__sun {
  transform-origin: center;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.theme-toggle--dark .theme-toggle__sun {
  transform: scale(1.8);
}

/* Sun rays */
.theme-toggle__rays {
  transform-origin: center;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1),
              opacity 0.3s ease;
}

.theme-toggle--dark .theme-toggle__rays {
  transform: rotate(45deg) scale(0);
  opacity: 0;
}

/* Moon eclipse mask */
.theme-toggle__moon {
  transform-origin: center;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateX(10px);
  fill: #050510;
}

.theme-toggle--dark .theme-toggle__moon {
  transform: translateX(-4px) translateY(4px);
}

/* Touch-friendly sizing on mobile */
@media (hover: none) {
  .theme-toggle {
    --toggle-size: 52px;
  }
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .theme-toggle__sun,
  .theme-toggle__rays,
  .theme-toggle__moon {
    transition-duration: 0.01ms;
  }
}
</style>
