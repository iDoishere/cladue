import { ref, onMounted, onUnmounted } from 'vue'

export interface TrailDot {
  x: number
  y: number
  id: number
  opacity: number
}

export function useCursorTrail() {
  const trail = ref<TrailDot[]>([])
  let trailId = 0

  function onMouseMove(e: MouseEvent) {
    const dot: TrailDot = { x: e.clientX, y: e.clientY, id: trailId++, opacity: 1 }
    trail.value.push(dot)
    setTimeout(() => {
      trail.value = trail.value.filter(d => d.id !== dot.id)
    }, 600)
  }

  onMounted(() => window.addEventListener('mousemove', onMouseMove))
  onUnmounted(() => window.removeEventListener('mousemove', onMouseMove))

  return { trail, onMouseMove }
}