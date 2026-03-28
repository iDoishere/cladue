<script setup lang="ts">
import type { TrailDot } from '../../composables/useCursorTrail'

defineProps<{
  trail: TrailDot[]
}>()
</script>

<template>
  <!-- Aurora background -->
  <div class="aurora">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
  </div>

  <!-- Cursor trail dots -->
  <div
    v-for="dot in trail"
    :key="dot.id"
    class="trail-dot"
    :style="{ left: dot.x + 'px', top: dot.y + 'px' }"
  ></div>
</template>

<style scoped>
.aurora {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.orb-1 {
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(124, 58, 237, 0.45) 0%, transparent 70%);
  top: -150px; left: -100px;
  animation: drift-1 14s ease-in-out infinite alternate;
}

.orb-2 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.35) 0%, transparent 70%);
  bottom: -100px; right: -80px;
  animation: drift-2 18s ease-in-out infinite alternate;
}

.orb-3 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(167, 139, 250, 0.25) 0%, transparent 70%);
  top: 40%; left: 50%;
  transform: translateX(-50%);
  animation: drift-3 22s ease-in-out infinite alternate;
}

@keyframes drift-1 {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(80px, 60px) scale(1.15); }
}
@keyframes drift-2 {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(-60px, -80px) scale(1.2); }
}
@keyframes drift-3 {
  from { transform: translateX(-50%) scale(1); opacity: 0.6; }
  to   { transform: translateX(-40%) scale(1.3); opacity: 1; }
}

.trail-dot {
  position: fixed;
  width: 12px; height: 12px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 999;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(167, 139, 250, 0.9) 0%, transparent 70%);
  box-shadow: 0 0 8px rgba(124, 58, 237, 0.6), 0 0 20px rgba(124, 58, 237, 0.3);
  animation: trail-fade 0.6s ease-out forwards;
}

@keyframes trail-fade {
  0%   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0; transform: translate(-50%, -50%) scale(0.2); }
}
</style>
